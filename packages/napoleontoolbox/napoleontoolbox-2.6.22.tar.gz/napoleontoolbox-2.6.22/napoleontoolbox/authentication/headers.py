__author__ = "hugo.inzirillo"

from abc import abstractmethod, ABCMeta

import requests
import requests.auth

from napoleontoolbox.authentication import Token, ClientCredentials, PasswordCredentials, Scope
from napoleontoolbox.authentication.auth_handler import NapoleonServiceAuthHandler
from napoleontoolbox.authentication.security_headers import AuthorizationHeader, ApplicationJsonHeader
from napoleontoolbox.dataloader.models import NapoleonService
from napoleontoolbox.napoleon_config_tools import getter


class AuthorizationHeaderManager(object):
    def __init__(self, token: Token):
        self.__token = token

    def build(self):
        return AuthorizationHeader.build(self.__token)


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

    @property
    @abstractmethod
    def authorization_header(self): ...


class AuthManagerTemplate(AbstractAuthManagerTemplate):
    def __init__(self):
        self.__url = str()
        self.__credentials = None
        self.__scope = Scope()
        self.__response = requests.Response
        self.__token = Token()
        self.__authorization_header = str()

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
    def authorization_header(self):
        return self.__authorization_header

    @authorization_header.setter
    def authorization_header(self, header: str):
        self.__authorization_header = header

    @property
    def token(self):
        return self.__token

    def _request(self) -> requests.Request: ...

    def _data(self): ...

    def _auth(self): ...

    def authenticate(self): ...


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


class NapoleonAuthenticationManager(AuthenticationManager):

    @property
    @getter(value="providers.napoleon_service.access_token_uri")
    def url(self):
        return self.url

    @property
    def credentials(self):
        return NapoleonService().get_credentials()

    @property
    def scope(self):
        return Scope(["READ", "WRITE"])

    def _handle_reponse(self):
        if self.response:
            if self.response.status_code == requests.codes.OK:
                _reponse = self.response.json()
                self.token = NapoleonServiceAuthHandler(_reponse).get_token()
                self.authorization_header = AuthorizationHeaderManager(self.token).build()


class NapoleonConnectorManager(object):

    def __init__(self):
        self.__authentication_manager = NapoleonAuthenticationManager()
        
    @property
    def authentication_manager(self):
        return self.__authentication_manager

    def execute_request(self):
        self.authentication_manager.authenticate()


if __name__ == '__main__':
    npx_auth_manager = NapoleonAuthenticationManager()
    npx_auth_manager.authenticate()

    end = True
