__author__ = "hugo.inzirillo"

from napoleontoolbox.napoleon_config_tools.parser import getter, config


@config
class Provider(object):
    """
    This object is set with config Attributes
    """

    def __init__(self):
        pass


class Bitmex(Provider):

    @property
    @getter("providers.bitmex.key")
    def key(self):
        return self.key

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
    @getter("providers.dropbox.key")
    def key(self):
        return self.key

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
    @getter("providers.binance.key")
    def key(self):
        return self.key

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
    @getter("providers.cryptocompare.key")
    def key(self):
        return self.key

    @property
    @getter("providers.cryptocompare.secret")
    def secret(self):
        return self.secret

    @property
    @getter("providers.cryptocompare.type")
    def type(self):
        return self.type


class Ressources(object):
    def __init__(self):
        self.__bitmex = Bitmex()
        self.__binance = Binance()
        self.__dropbox = Dropbox()
        self.__cryptocompare = CryptoCompare()

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
