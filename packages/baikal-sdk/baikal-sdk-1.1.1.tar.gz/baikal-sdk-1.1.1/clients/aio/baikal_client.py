"""Asynchronous Http clients to get tokens from 4P authserver using OIDC protocol"""

__author__ = '4th Platform team'
__license__ = "see LICENSE file"

import logging
import random
import clients.aio.aiohttp_client as aiohttp_client
from aiohttp import BasicAuth, ClientTimeout, ClientError
from datetime import timedelta
from clients.baikal_client import is_truethy, load_jwk_set, build_jwt_payload, verify_signature, build_jwk_set, \
    AuthserverConfig
from os import getenv
from aiocache import cached
from async_property import async_property

from clients.exceptions import ConfigurationError, AuthserverError

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
ASSERTION_EXP_GAP = timedelta(minutes=60)
DEFAULT_REQUEST_TIMEOUT = 15  # timeout in seconds to wait for a response from authserver
TTL_CACHE = 15 * 60
NTTL_CACHE = 20 * 60
SIZE_CACHE = 10


# TODO: add nttl and max_size
@cached(ttl=TTL_CACHE)
async def get_authserver_config(authserver_endpoint, verify_certs=True):
    """
    It returns the configuration needed in our client of the authserver 4P:
        token endpoint and public keys in jwk format
    :param verify_certs:
    :param authserver_endpoint:
    :return: namedtupl
    """
    if authserver_endpoint.endswith('/'):
        authserver_endpoint = authserver_endpoint[:-1]

    well_known_uri = authserver_endpoint + "/.well-known/openid-configuration"
    try:
        async with aiohttp_client.get(well_known_uri, ssl=verify_certs) as r:
            config = await r.json()
        token_endpoint = config['token_endpoint']
        authorization_endpoint = config['authorization_endpoint']
        issuer = config['issuer']
        jwks_uri = config['jwks_uri']
        introspection_endpoint = config['introspection_endpoint']
        introspection_auth = config['introspection_endpoint_auth_methods_supported']
        async with aiohttp_client.get(jwks_uri, ssl=verify_certs) as r:
            jwks = await r.json()

        return AuthserverConfig(issuer=issuer,
                                token_endpoint=token_endpoint,
                                authorization_endpoint=authorization_endpoint,
                                jwks=jwks,
                                introspection_endpoint=introspection_endpoint,
                                introspection_auth=introspection_auth)
    except Exception as e:
        msg = "Error getting authserver configuration: {}".format(str(e))
        logger.error(msg)
        raise AuthserverError(msg)


class OpenIDClient(object):

    def __init__(self, authserver_endpoint=None, client_id=None, client_secret=None, client_keys=None, issuer=None,
                 private_certs_path=None):
        self.verify_certs = is_truethy(getenv('BAIKAL_VERIFY_CERTS'))
        self._authserver_endpoint = getenv('BAIKAL_AUTHSERVER_ENDPOINT') or authserver_endpoint
        self._client_id = getenv('BAIKAL_CLIENT_ID') or client_id
        self._client_secret = getenv('BAIKAL_CLIENT_SECRET') or client_secret
        self._sanity_check()

        self._authserver_auth = BasicAuth(login=self._client_id, password=self._client_secret, encoding='UTF-8')
        self.issuer = getenv('BAIKAL_ISSUER') or issuer
        self.private_keys, self.public_keys = load_jwk_set(getenv('BAIKAL_PRIVATE_CERTS_PATH') or private_certs_path,
                                                           getenv('BAIKAL_CLIENT_KEYS') or client_keys)

    def _sanity_check(self):
        if not self._authserver_endpoint:
            raise ConfigurationError("authserver endpoint not configured")

        if not self._client_id:
            raise ConfigurationError("client_id not configured")

        if not self._client_secret:
            raise ConfigurationError("client_secret not configured")

    @async_property
    async def authserver_config(self):
        return await get_authserver_config(self._authserver_endpoint, verify_certs=self.verify_certs)

    def get_random_key(self):
        return random.choice(self.private_keys['keys'])

    async def grant_user(self, sub, scopes, purposes, authorization_id=None, identifier=None, acr=None,
                         authentication_context=None, headers={}, timeout=DEFAULT_REQUEST_TIMEOUT,
                         full_authserver_response=False):
        if not self.issuer:
            raise ConfigurationError("Issuer should be defined to generate tokens with jwt-bearer")
        if not self.private_keys['keys']:
            raise ConfigurationError("No private keys found for generating assertion")

        authserver_config = await self.authserver_config
        assertion = build_jwt_payload(sub, scopes, purposes, self.issuer, authserver_config.issuer,
                                      self.get_random_key(), authorization_id=authorization_id, identifier=identifier,
                                      authentication_context=authentication_context, acr=acr)
        body = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': assertion
        }

        return await self._call_token_endpoint(body, headers, timeout,
                                               full_authserver_response=full_authserver_response)

    async def grant_client(self, scopes=None, purposes=None, headers={}, timeout=DEFAULT_REQUEST_TIMEOUT,
                           full_authserver_response=False):
        body = {
            'grant_type': 'client_credentials'
        }
        if scopes:
            body['scope'] = ' '.join(scopes)
        if purposes:
            body['purposes'] = ' '.join(purposes)
        return await self._call_token_endpoint(body, headers, timeout,
                                               full_authserver_response=full_authserver_response)

    async def authorize(self, scopes=None, purposes=None, redirect_uri=None, **extra_params):
        authserver_config = await self.authserver_config
        authorization_url = \
            f"{authserver_config.authorization_endpoint}?response_type=code&client_id={self._client_id}"
        if scopes:
            authorization_url = f"{authorization_url}&scope={' '.join(scopes)}"
        if purposes:
            authorization_url = f"{authorization_url}&purpose={' '.join(purposes)}"
        if not redirect_uri:
            raise AuthserverError("redirect_uri field is mandatory")
        authorization_url = f"{authorization_url}&redirect_uri={redirect_uri}"
        extra_params_builder = [f"{key}={value}" for key, value in extra_params.items()]
        if extra_params_builder:
            authorization_url = f"{authorization_url}&{'&'.join(extra_params_builder)}"
        return authorization_url

    async def grant_code(self, code=None, redirect_uri=None, headers={}, timeout=DEFAULT_REQUEST_TIMEOUT,
                         full_authserver_response=False):
        if not code:
            raise AuthserverError("code field is mandatory")
        if not redirect_uri:
            raise AuthserverError("redirect_uri field is mandatory")
        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }
        return await self._call_token_endpoint(body, headers, timeout,
                                               full_authserver_response=full_authserver_response)

    async def introspect(self, access_token, timeout=DEFAULT_REQUEST_TIMEOUT):
        authserver_config = await self.authserver_config
        try:
            async with aiohttp_client.post(authserver_config.introspection_endpoint, data={'token': access_token},
                                           auth=self._authserver_auth, ssl=self.verify_certs,
                                           timeout=ClientTimeout(total=timeout)) as r:
                if r.status != 200:
                    raise AuthserverError("Error from token introspection endpoint of Authserver: " +
                                          await self._parse_error(r))
                return await r.json()
        except ClientError as e:
            raise AuthserverError(str(e))

    @staticmethod
    async def _parse_error(response):
        try:
            error = await response.json()
            return str(error)
        except:
            text = await response.text()
            return f"Unexpected response from authserver: status_code {response.status}; resp: {text}"

    async def _call_token_endpoint(self, body, headers, timeout, full_authserver_response=False):
        authserver_config = await self.authserver_config
        try:
            async with aiohttp_client.post(authserver_config.token_endpoint, data=body, auth=self._authserver_auth,
                                           headers=headers, ssl=self.verify_certs,
                                           timeout=ClientTimeout(total=timeout)) as r:
                if r.status == 401:
                    raise AuthserverError("The credentials client_id/client_secret are invalid.")
                elif r.status != 200:
                    raise AuthserverError("Error from token endpoint of Authserver: " + await self._parse_error(r))
                body = await r.json()
        except ClientError as e:
            raise AuthserverError(str(e))

        return body if full_authserver_response else body['access_token']

    async def verify_signature(self, id_token):
        authserver_config = await self.authserver_config
        return verify_signature(id_token, authserver_config.jwks)

    def get_jwk_set(self, dump_json=True):
        return build_jwk_set(self.public_keys['keys'], dump_json=dump_json)
