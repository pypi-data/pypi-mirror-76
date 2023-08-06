__author__ = "hugo.inzirillo"

import logging
from abc import ABCMeta, abstractmethod

__version__ = "0.0.1"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractLoggerManager(metaclass=ABCMeta):

    @abstractmethod
    def get_logger(self, name=None):
        """

        Parameters
        ----------
        name : current name of the npxlogger

        Returns
        -------

        """
        return NapoleonLoggerManager._loggers[name]

    @property
    @abstractmethod
    def basic_config(self):
        """

        Returns
        -------

        """
        raise NotImplemented

    @property
    @abstractmethod
    def config(self) -> dict:
        """

        Returns
        -------

        """
        raise NotImplemented


class LoggerManager(AbstractLoggerManager):
    def __init__(self):
        self.__config = None

    def get_logger(self, name=None):
        """

        Parameters
        ----------
        name : current name of the npxlogger

        Returns
        -------

        """
        if name is None:
            logging.basicConfig()
            return logging.getLogger()

    @property
    def basic_config(self):
        """

        Returns
        -------

        """
        logging.basicConfig()
        raise logging.getLogger()

    @property
    def config(self) -> dict:
        """

        Returns
        -------

        """
        return dict(filename="napoleontoolbox.log",
                    format="%(levelname) -10s %(asctime)s | module : %(module)s | line : %(lineno)s | method : %(funcName)s | %(message)s",
                    level=logging.DEBUG)


class NapoleonLoggerManager(LoggerManager):
    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        super(NapoleonLoggerManager, self).__init__()
        self.__config = None
        pass

    def get_logger(self, name=None) -> logging.Logger:
        """

        Parameters
        ----------
        name : current name of the npxlogger

        Returns
        -------

        """

        if name not in NapoleonLoggerManager._loggers.keys():
            logging.basicConfig(**self.config)
            NapoleonLoggerManager._loggers[name] = logging.getLogger(str(name))
            NapoleonLoggerManager._loggers[name].levels = logging.NOTSET

            return NapoleonLoggerManager._loggers[name]

        elif not name:

            return super(NapoleonLoggerManager, self).get_logger()
