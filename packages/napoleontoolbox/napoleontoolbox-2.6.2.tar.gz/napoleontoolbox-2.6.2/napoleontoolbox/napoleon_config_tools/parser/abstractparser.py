__author__ = "hugo.inzirillo"

from abc import (
    ABCMeta, abstractmethod,abstractproperty
)

from napoleontoolbox.napoleon_config_tools.model.config import Config


class AbstractParserTemplate(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load') and
                callable(subclass.load) and
                hasattr(subclass, 'existing') and
                callable(subclass.existing) and
                hasattr(subclass, 'read_file') and
                callable(subclass.read_file) or
                NotImplemented)

    @abstractmethod
    def load(self):
        """
        This method will look up the yaml file attached to your profile
        Returns
        -------

        """
        raise NotImplemented

    @abstractmethod
    def existing(self):
        """
        This method will check the existence of a config file
        Returns
        -------

        """
        raise NotImplemented

    @abstractmethod
    def read_file(self):
        """
        This method will read the config file yaml
        Returns
        -------

        """
        raise NotImplemented

    @property
    @abstractmethod
    def config(self) -> Config: raise NotImplemented