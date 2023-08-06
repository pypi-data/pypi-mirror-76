__author__ = "hugo.inzirillo"

from abc import abstractmethod, ABCMeta

from napoleontoolbox.bifrost import Token


class AbstractAuthResponseHandlerTemplate(metaclass=ABCMeta):

    @property
    @abstractmethod
    def _response(self):
        raise NotImplemented

    @abstractmethod
    def _get_token(self):
        raise NotImplemented

    @abstractmethod
    def _get_token_type(self):
        raise NotImplemented

    @abstractmethod
    def get_token(self):
        raise NotImplemented


class AuthResponseHandlerTemplate(AbstractAuthResponseHandlerTemplate):
    def __init__(self, _reponse: dict):
        self.__reponse = _reponse

    @property
    def _response(self):
        return self.__reponse

    def _get_token(self): ...

    def _get_token_type(self): ...

    def get_token(self): ...


class NapoleonServiceAuthHandler(AuthResponseHandlerTemplate):

    def _get_token(self):
        return self._response["access_token"]

    def _get_token_type(self):
        return str(self._response["token_type"]).capitalize()

    def get_token(self):
        _token = Token()
        _token.value = self._get_token()
        _token.type = self._get_token_type()
        return _token
