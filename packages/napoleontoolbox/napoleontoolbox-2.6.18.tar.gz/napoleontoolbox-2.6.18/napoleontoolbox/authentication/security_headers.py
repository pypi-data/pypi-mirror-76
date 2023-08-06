__author__ = "hugo.inzirillo"

from abc import abstractmethod, ABCMeta
from typing import Union

import requests.auth

from napoleontoolbox.authentication import ClientCredentials, PasswordCredentials, Token


class AbstractHeaderTemplate(metaclass=ABCMeta):

    @property
    @abstractmethod
    def value(self):
        raise NotImplemented

    @staticmethod
    def build(object: Union[PasswordCredentials, ClientCredentials, Token]):
        raise NotImplemented


class AbstractHeaders(AbstractHeaderTemplate):

    @property
    @abstractmethod
    def value(self):
        raise NotImplemented

    @staticmethod
    def build(object: Union[PasswordCredentials, ClientCredentials, Token]):
        raise NotImplemented


class AbstractHeadersScheme(AbstractHeaderTemplate):

    @property
    @abstractmethod
    def value(self):
        raise NotImplemented

    @classmethod
    def build(self, object: Union[PasswordCredentials, ClientCredentials, Token]):
        raise NotImplemented


class HeadersScheme(AbstractHeaderTemplate):

    def __init__(self, o: Union[Token] = None):
        self.__object = o
        self.__header = None
        self.__auth = requests.auth.HTTPBasicAuth

    @property
    def object(self):
        return self.__object

    @property
    def value(self):
        return self.__header

    @value.setter
    def value(self, value: dict):
        self.__header = value

    def build(self):
        return self


class AuthorizationHeaderScheme(HeadersScheme):
    def build(self):
        if isinstance(self.object, Token):
            self.value = {
                "Authorization": "{type} {token_value}".format(type=self.object.type, token_value=self.object.value)}
        return self


class JsonHeaderScheme(HeadersScheme):
    def build(self):
        self.value = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        return self


class TemplateHeaders(AbstractHeaders):

    def value(self): ...

    @staticmethod
    def build(object: Union[PasswordCredentials, ClientCredentials, Token]): ...


class Headers(TemplateHeaders):
    def __init__(self):
        self.__content = None
        self.__value = dict()

    @property
    def value(self) -> dict:
        return self.__value

    def __dict__(self):
        return self.__value

    @staticmethod
    def build(o: Union[PasswordCredentials, ClientCredentials, Token] = None):
        return HeaderGenerator().build(o).value


class HeaderGenerator(AbstractHeaders):
    def __init__(self):
        self.__header = None

    @property
    def value(self):
        return self.__header

    def build(self, object: Union[Token] = None):

        if object:
            if isinstance(self.__header.content, Token):
                self.__header = AuthorizationHeaderScheme(object).build().value

        else:
            self.__header = JsonHeaderScheme().build().value
        return self


class ApplicationJsonHeader(Headers):
    pass


class AuthorizationHeader(Headers):
    pass
