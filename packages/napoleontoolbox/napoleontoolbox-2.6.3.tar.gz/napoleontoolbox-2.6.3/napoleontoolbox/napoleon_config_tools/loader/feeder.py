__author__ = "hugo.inzirillo"

import os

import yaml

from napoleontoolbox import __path__
from napoleontoolbox.napoleon_config_tools.object.config import Config
from napoleontoolbox.napoleon_config_tools.loader.abstractfeeder import AbstractYamlReader
from npxlogger import log


class YamlReader(AbstractYamlReader):
    def __init__(self):
        self.__raw_config = None
        pass

    def _read(self, _path: str):
        """

        Parameters
        ----------
        _path : path of file to read .yml

        Returns
        -------

        """
        with open(_path, 'r') as stream:
            try:
                self.__raw_config = yaml.safe_load(stream)
                log.info("reading current config : {conf}".format(conf=self.__raw_config))
            except yaml.YAMLError as exc:
                log.error(exc)

    @property
    def raw_config(self):
        return self.__raw_config


class NapoleonConfigReader(YamlReader):

    @property
    def __config_file_path(self):
        return os.path.join(__path__[0], Config.FILE)

    def _read(self, _path: str = None):
        """

        Parameters
        ----------
        _path : path of file to read .yml

        Returns
        -------

        """

        if _path is not None:
            path = _path
        else:
            path = self.__config_file_path

        return super(NapoleonConfigReader, self)._read(path)

    def read(self, _path: str = None):
        """
        This method read the config.yml file
        Returns
        -------

        """

        return self._read(_path)
