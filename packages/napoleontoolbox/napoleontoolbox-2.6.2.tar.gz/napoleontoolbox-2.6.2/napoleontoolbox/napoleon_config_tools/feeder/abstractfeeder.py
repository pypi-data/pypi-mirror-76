__author__ = "hugo.inzirillo"

from abc import ABCMeta, abstractmethod


class AbstractYamlReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self, _path: str):
        """

        Returns
        -------

        """

        raise NotImplemented


class YamlReader(AbstractYamlReader):
    def __init__(self):
        pass

    def read(self, _path: str):
        """

        Parameters
        ----------
        _path : path of file to read .yml

        Returns
        -------

        """
        pass


class NapoleonConfigReader(YamlReader):
    def read(self, _path: str):
        """

        Parameters
        ----------
        _path : path of file to read .yml

        Returns
        -------

        """
        pass

