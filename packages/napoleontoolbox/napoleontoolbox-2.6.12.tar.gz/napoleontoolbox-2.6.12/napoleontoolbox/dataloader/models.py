__author__ = "hugo.inzirillo"

from abc import ABCMeta, abstractmethod

from napoleontoolbox.napoleon_config_tools import getter, config


class AbsctractRessource(metaclass=ABCMeta):

    @property
    @abstractmethod
    def id(self):
        raise NotImplemented

    @property
    @abstractmethod
    def secret(self):
        raise NotImplemented

    @property
    @abstractmethod
    def type(self):
        raise NotImplemented

    @property
    @abstractmethod
    def user(self):
        raise NotImplemented

    @property
    @abstractmethod
    def password(self):
        raise NotImplemented


@config
class Service(AbsctractRessource):
    def __init__(self):
        self.__id = None
        self.__secret = None
        self.__type = None
        self.__user = None
        self.__password = None

    @property
    def id(self):
        return self.id

    @property
    def secret(self):
        return self.secret

    @property
    def type(self):
        return self.type

    @property
    def user(self):
        return self.user

    @property
    def password(self):
        return self.password


@config
class Provider(AbsctractRessource):
    def __init__(self):
        self.__id = None
        self.__secret = None
        self.__type = None

    @property
    def type(self):
        return self.type

    @property
    def id(self):
        return self.id

    @property
    def secret(self):
        return self.secret

    def user(self):
        pass

    def password(self):
        pass


class Bitmex(Provider):

    @property
    @getter("providers.bitmex.id")
    def id(self):
        return self.id

    @property
    @getter("providers.bitmex.secret")
    def secret(self):
        return self.secret

    @property
    @getter("providers.bitmex.type")
    def type(self):
        return self.type


class Dropbox(Provider):

    @property
    @getter("providers.dropbox.id")
    def id(self):
        return self.id

    @property
    @getter("providers.dropbox.secret")
    def secret(self):
        return self.secret

    @property
    @getter("providers.dropbox.type")
    def type(self):
        return self.type


class Binance(Provider):

    @property
    @getter("providers.binance.id")
    def id(self):
        return self.id

    @property
    @getter("providers.binance.secret")
    def secret(self):
        return self.secret

    @property
    @getter("providers.binance.type")
    def type(self):
        return self.type


class CryptoCompare(Provider):

    @property
    @getter("providers.cryptocompare.id")
    def id(self):
        return self.id

    @property
    @getter("providers.cryptocompare.secret")
    def secret(self):
        return self.secret

    @property
    @getter("providers.cryptocompare.type")
    def type(self):
        return self.type


class NapoleonService(Service):

    @property
    @getter("providers.napoleon_service.id")
    def id(self):
        return self.id

    @property
    @getter("providers.napoleon_service.secret")
    def secret(self):
        return self.secret

    @property
    @getter("providers.napoleon_service.type")
    def type(self):
        return self.type

    @property
    @getter("providers.napoleon_service.user")
    def user(self):
        return self.user

    @property
    @getter("providers.napoleon_service.password")
    def password(self):
        return self.password


class Ressources(object):
    def __init__(self):
        self.__bitmex = Bitmex
        self.__binance = Binance
        self.__dropbox = Dropbox
        self.__cryptocompare = CryptoCompare
        self.__napoleon_service = NapoleonService

    @property
    def bitmex(self):
        return self.__bitmex

    @property
    def binance(self):
        return self.__binance

    @property
    def cryptocompare(self):
        return self.__cryptocompare

    @property
    def dropbox(self):
        return self.__dropbox

    @property
    def napoleon_service(self):
        return self.__napoleon_service
