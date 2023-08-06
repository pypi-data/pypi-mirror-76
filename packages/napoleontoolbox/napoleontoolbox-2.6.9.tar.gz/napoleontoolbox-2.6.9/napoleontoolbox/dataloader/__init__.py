__author__ = "hugo.inzirillo"

from napoleontoolbox.dataloader.models import Ressources, Dropbox, Bitmex, Binance, CryptoCompare, Provider

__all__ = ['Ressources',
           'Dropbox',
           'Bitmex',
           'Binance',
           'CryptoCompare',
           'Provider']


class DataLoader(object):
    def __init__(self):
        self.__ressources = Ressources()

    @property
    def ressources(self):
        return self.__ressources
