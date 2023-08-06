"""Http clients to get tokens from 4P authserver using OIDC protocol"""
__author__ = '4th Platform team'
__license__ = "see LICENSE file"

import ujson as json
import logging
import random
from collections import namedtuple
from datetime import timedelta, datetime
from pathlib import Path
from os import getenv

import requests
from jose import jwt, jws, JWSError
from jose.backends import RSAKey, ECKey
from jose.constants import ALGORITHMS
from requests.auth import HTTPBasicAuth

from clients.cache import lru_cache
from clients.exceptions import ConfigurationError, AuthserverError, InvalidSignature

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
AuthserverConfig = namedtuple('AuthserverConfig', ['issuer', 'token_endpoint', 'authorization_endpoint', 'jwks',
                                                   'introspection_endpoint', 'introspection_auth'])
ASSERTION_EXP_GAP = timedelta(minutes=60)
DEFAULT_REQUEST_TIMEOUT = 15  # timeout in seconds to wait for a response from authserver
TTL_CACHE = 15 * 60
NTTL_CACHE = 20 * 60
SIZE_CACHE = 10


@lru_cache(max_size=SIZE_CACHE, ttl=TTL_CACHE, nttl=NTTL_CACHE)
def get_authserver_config(authserver_endpoint, verify_certs=True):
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
        r = requests.get(well_known_uri, verify=verify_certs)
        config = r.json()
        token_endpoint = config['token_endpoint']
        authorization_endpoint = config['authorization_endpoint']
        issuer = config['issuer']
        jwks_uri = config['jwks_uri']
        introspection_endpoint = config['introspection_endpoint']
        introspection_auth = config['introspection_endpoint_auth_methods_supported']
        r = requests.get(jwks_uri, verify=verify_certs)
        jwks = r.json()
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


def guess_key(key_path):
    """
    Guess the key format of the key in path given and return the  key
    :param key_path:
    :return:
    """

    # Try RSA keys (most common with hassh SHA256 -> RS256 alg)
    try:
        key_content = Path(key_path).read_text()
        key = RSAKey(key_content, ALGORITHMS.RS256)
        if key.is_public():
            logger.debug("RSA public key %s ignored", key_path)
            return None
        key.to_dict()
        return key
    except Exception as e:
        logger.debug("RSA key %s invalid: %s", key_path, str(e))

    # Try EC keys (most common with hassh SHA256 -> ES256 alg)
    try:
        key_content = Path(key_path).read_text()
        key = ECKey(key_content, ALGORITHMS.ES256)
        if key.is_public():
            logger.debug("EC public key %s ignored", key_path)
            return None
        key.to_dict()
        return key
    except Exception as e:
        logger.debug("EC key %s invalid: %s", key_path, str(e))

    return None


def load_jwk_set(path, keys):
    """
    It builds  JWKS set, (private and public) with the private keys found that will be used for signing assertions in jwt-bearer and expose the set in public format
    :param path: path to all private keys files
    :param keys: list of keys in string format
    :return: a tuple with private and public keys in dict format following JWK format
    """
    keys_private = []
    keys_public = []
    if path:
        for filename in Path(path).iterdir():
            key = guess_key(filename)
            if not key:
                logger.warning("The key %s is not supported", filename)
            else:
                keys_private.append(key.to_dict())
                keys_public.append(key.public_key().to_dict())

    return {'keys': keys_private}, {'keys': keys_public}


def ensure_string(in_bytes):
    try:
        return in_bytes.decode('UTF-8')
    except Exception:
        return in_bytes


def is_truethy(var):
    return var not in ('False', 'false', False)


def verify_signature(id_token, jwks):
    try:
        header = jws.get_unverified_header(id_token)
        jws.verify(id_token, jwks, header['alg'])
    except JWSError as e:
        raise InvalidSignature("Error verifying signature of id_token: " + str(e))


def build_jwt_payload(sub, scopes, purposes, issuer, audience, key, authorization_id=None, identifier=None,
                      acr=None, authentication_context=None):
    now = datetime.utcnow()  # jose library converts to epoch time
    payload = {
        'sub': sub,
        'active': True,
        'scope': ' '.join(scopes),
        'purpose': ' '.join(purposes),
        'exp': now + ASSERTION_EXP_GAP,
        'iat': now,
        'iss': issuer,
        'aud': audience
    }
    if authorization_id:
        payload['authorization_id'] = authorization_id

    if identifier:
        payload['identifier'] = identifier

    if acr:
        payload['acr'] = acr
    if authentication_context:
        payload['authentication_context'] = authentication_context

    assertion = jwt.encode(payload, key, algorithm=key['alg'])
    return assertion


def build_jwk_set(public_keys, dump_json=True):
    public_key_jwk_serialized = map(lambda key: {k: ensure_string(v) for k, v in key.items()}, public_keys)
    jwk_set = {'keys': list(public_key_jwk_serialized)}
    return json.dumps(jwk_set) if dump_json else jwk_set


class OpenIDClient(object):

    def __init__(self, authserver_endpoint=None, client_id=None, client_secret=None, client_keys=None, issuer=None,
                 private_certs_path=None):
        self.verify_certs = is_truethy(getenv('BAIKAL_VERIFY_CERTS'))
        if not self.verify_certs:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._authserver_endpoint = getenv('BAIKAL_AUTHSERVER_ENDPOINT') or authserver_endpoint
        self._client_id = getenv('BAIKAL_CLIENT_ID') or client_id
        self._client_secret = getenv('BAIKAL_CLIENT_SECRET') or client_secret
        self._sanity_check()

        self._authserver_auth = HTTPBasicAuth(self._client_id, self._client_secret)
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

    @property
    def authserver_config(self):
        return get_authserver_config(self._authserver_endpoint, verify_certs=self.verify_certs)

    def get_random_key(self):
        return random.choice(self.private_keys['keys'])

    def grant_user(self, sub, scopes, purposes, authorization_id=None, identifier=None, headers={},
                   timeout=DEFAULT_REQUEST_TIMEOUT, full_authserver_response=False):
        if not self.issuer:
            raise ConfigurationError("Issuer should be defined to generate tokens with jwt-bearer")
        if not self.private_keys['keys']:
            raise ConfigurationError("No private keys found for generating assertion")

        assertion = build_jwt_payload(sub, scopes, purposes, self.issuer, self.authserver_config.issuer,
                                      self.get_random_key(), authorization_id=authorization_id, identifier=identifier)
        body = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': assertion
        }

        return self._call_token_endpoint(body, headers, timeout, full_authserver_response=full_authserver_response)

    def grant_client(self, scopes=None, purposes=None, headers={}, timeout=DEFAULT_REQUEST_TIMEOUT,
                     full_authserver_response=False):
        body = {
            'grant_type': 'client_credentials'
        }
        if scopes:
            body['scope'] = ' '.join(scopes)
        if purposes:
            body['purposes'] = ' '.join(purposes)
        return self._call_token_endpoint(body, headers, timeout, full_authserver_response=full_authserver_response)

    def authorize(self, scopes=None, purposes=None, redirect_uri=None, **extra_params):
        authorization_url = f"{self.authserver_config.authorization_endpoint}?response_type=code&client_id={self._client_id}"
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

    def grant_code(self, code=None, redirect_uri=None, headers={}, timeout=DEFAULT_REQUEST_TIMEOUT,
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
        return self._call_token_endpoint(body, headers, timeout, full_authserver_response=full_authserver_response)

    def introspect(self, access_token, timeout=DEFAULT_REQUEST_TIMEOUT):
        r = requests.post(self.authserver_config.introspection_endpoint, {'token': access_token},
                          auth=self._authserver_auth, verify=self.verify_certs, timeout=timeout)
        if r.status_code!= requests.codes.ok:
            raise AuthserverError("Error from,,,introspection endpoint:" + self._parse_error(r))
        return r.json()

    @staticmethod
    def _parse_error(response):
        try:
            error = response.json()
            return str(error)
        except ValueError:
            return "Unexpected response from authserver: status_code {}; resp: {}".format(response.status_code, response.text)

    def _call_token_endpoint(self, body, headers, timeout, full_authserver_response=False):
        r = requests.post(self.authserver_config.token_endpoint, body, auth=self._authserver_auth,
                          verify=self.verify_certs, headers=headers, timeout=timeout)
        if r.status_code == requests.codes.unauthorized:
            raise AuthserverError("The credentials client_id/client_secret are invalid.")
        elif r.status_code != requests.codes.ok:
            raise AuthserverError("Error from token endpoint of Authserver: " + self._parse_error(r))

        body = r.json()
        return body if full_authserver_response else body['access_token']

    def _verify_signature(self, id_token):
        return verify_signature(id_token, self.authserver_config.jwks)

    def get_jwk_set(self, dump_json=True):
        return build_jwk_set(self.public_keys['keys'], dump_json=dump_json)
