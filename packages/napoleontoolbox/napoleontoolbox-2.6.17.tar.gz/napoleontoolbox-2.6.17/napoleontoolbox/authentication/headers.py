__author__ = "hugo.inzirillo"

from abc import abstractmethod, ABCMeta
from typing import Union

import requests
import requests.auth

from napoleontoolbox.authentication import Token, ClientCredentials, PasswordCredentials, Scope
from napoleontoolbox.authentication.auth_handler import NapoleonServiceAuthHandler
from napoleontoolbox.authentication.security_headers import AuthorizationHeader, ApplicationJsonHeader


class AuthorizationHeaderManager(object):
    def __init__(self, token: Token):
        self.__value = token.value

    def build(self):
        return AuthorizationHeader.build(self.__value)


class AbstractAuthManagerTemplate(metaclass=ABCMeta):

    @abstractmethod
    def authenticate(self) -> Token: ...

    @abstractmethod
    def _request(self) -> requests.Request: ...

    @abstractmethod
    def _handle_reponse(self) -> requests.Request: ...

    @abstractmethod
    def _data(self): ...

    @abstractmethod
    def _auth(self): ...

    @property
    @abstractmethod
    def response(self): ...

    @property
    @abstractmethod
    def token(self): ...


class AuthManagerTemplate(AbstractAuthManagerTemplate):
    def __init__(self, url: str, credentials: Union[ClientCredentials, PasswordCredentials], scope: Scope = None):
        self.__url = url
        self.__credentials = credentials
        self.__scope = scope
        self.__response = requests.Response
        self.__token = Token()

    @property
    def url(self):
        return self.__url

    @property
    def credentials(self):
        return self.__credentials

    @property
    def scope(self):
        return self.__scope

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, response):
        self.__response = response

    @property
    def token(self):
        return self.__token

    def _request(self) -> requests.Request: ...

    def _data(self): ...

    def _auth(self): ...

    def authenticate(self) -> AbstractAuthManagerTemplate:
        pass


class AuthenticationManager(AuthManagerTemplate):

    def _auth(self):
        return requests.auth.HTTPBasicAuth(self.credentials.client_id, self.credentials.client_secret)

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token

    def _data(self):
        _temp = None
        if isinstance(self.credentials, ClientCredentials):
            _temp = {"grant_type": "{grant_type}"}
            _temp.update({"grant_type": self.credentials.__repr__()})
        elif isinstance(self.credentials, PasswordCredentials):
            _temp = {"username": "{username}", "password": "{password}", "grant_type": "{grant_type}"}
            _temp.update(
                {"username": self.credentials.user, "password": self.credentials.password,
                 "grant_type": self.credentials.__repr__()}
            )
        if _temp:
            return _temp
        return {}

    def _request_token(self):
        if self.url and self.credentials and self.scope:
            self.response = self._request()
            self._handle_reponse()

    def _handle_reponse(self):
        raise NotImplemented

    def _request(self):
        return requests.post(url=self.url, headers=ApplicationJsonHeader().build(), auth=self._auth(),
                             data=self._data())

    def authenticate(self):
        self._request_token()

        return self


class NapoleonAuthenticationManager(AuthenticationManager):

    def _handle_reponse(self):
        if self.response:
            if self.response.status_code == requests.codes.OK:
                _reponse = self.response.json()
                self.token = NapoleonServiceAuthHandler(_reponse).get_token()



