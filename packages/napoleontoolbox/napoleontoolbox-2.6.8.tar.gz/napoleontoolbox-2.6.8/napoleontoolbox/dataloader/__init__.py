__author__ = "hugo.inzirillo"

from napoleontoolbox.dataloader.models import Ressources, Dropbox, Bitmex


class DataLoader(object):
    def __init__(self):
        self.__ressources = Ressources()

    @property
    def ressources(self):
        return self.__ressources


if __name__ == '__main__':
    test = DataLoader()
    end = True
