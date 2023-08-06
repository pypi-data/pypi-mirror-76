__author__ = "hugo.inzirillo"

from abc import abstractmethod

from napoleontoolbox.napoleon_config_tools.loader.feeder import NapoleonConfigReader
from napoleontoolbox.napoleon_config_tools.object.config import Config
from napoleontoolbox.napoleon_config_tools.object.environment import Env
from napoleontoolbox.napoleon_config_tools.parser.abstractparser import AbstractParserTemplate
from napoleontoolbox.napoleon_config_tools.loader import Profile
from npxlogger import log


class ParserTemplate(AbstractParserTemplate):

    @abstractmethod
    def _load(self):
        """
        This method will look up the yaml file attached to your loader
        Returns
        -------

        """
        raise NotImplemented

    @abstractmethod
    def _existing(self):
        """
        This method will check the existence of a config file
        Returns
        -------

        """
        raise NotImplemented

    @abstractmethod
    def _read_file(self):
        """
        This method will read the config file yaml
        Returns
        -------

        """
        raise NotImplemented

    @property
    @abstractmethod
    def config(self) -> Config:
        """
        This property return the Config
        Returns
        -------

        """
        raise NotImplemented

    @property
    @abstractmethod
    def feeder(self):
        """
        This property return the Feeder
        Returns
        -------

        """
        raise NotImplemented


class Parser(ParserTemplate):

    def __init__(self):
        self.__config = None
        self.__feeder = None

    def _load(self):
        """
        This method will look up the yaml file attached to your loader
        Returns
        -------

        """
        pass

    def _existing(self):
        """
        This method will check the existence of a config file
        Returns
        -------

        """
        pass

    def _read_file(self):
        """
        This method will read the config file yaml
        Returns
        -------

        """
        pass

    @property
    def config(self) -> Config:
        """
        This property return the Config
        Returns
        -------

        """
        return self.__config

    @property
    def feeder(self):
        """
        This property return the Feeder
        Returns
        -------

        """
        return self.__feeder


@Profile(Env.TEST.value)
class NapoleonToolboxConfigParser(Parser):

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, _conf: Config):
        self.__config = _conf

    def parse(self) -> Config:
        """
        This method will parse the config and return a Config object
        Returns
        -------

        """
        return self._load()

    def _load(self):
        """
        This method will look up the yaml file attached to your loader
        Returns
        -------

        """

        return self._existing()

    def _existing(self):
        """
        This method will check the existence of a config file
        Returns
        -------

        """
        return self._read_file()

    def _read_file(self):
        """
        This method will read the config file yaml
        Returns
        -------

        """

        log.info("current loader : {config}".format(config=self.config))
        return NapoleonConfigReader().read()
