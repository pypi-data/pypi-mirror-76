import json

from napoleontoolbox.napoleon_config_tools.object.modelparamtemplate import ModelParamTemplate
from npxlogger import log


# todo make meta dict


class Config(object):
    FILE = "config_test"

    def __init__(self):
        self.__profile = None
        self.__isrunnable = bool()
        self.__package = str()
        self.__model_parameters = ModelParamTemplate()
        self.__config_value = ""

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.__dict__())

    def __dict__(self):
        return dict(profile=self.__profile,
                    isrunnable=self.__isrunnable,
                    package=self.__package,
                    model_parameters=self.__model_parameters.__dict__())

    @staticmethod
    def value(_value: str):
        def inner_function(function):
            def wrapper(*args, **kwargs):
                log.info("target value in config :  {value}".format(value=_value))
                function(*args, **kwargs)

            return wrapper

        return inner_function

    @staticmethod
    def __look_up(_value: str):
        _path = _value.split(".")

    @property
    def profile(self) -> str:
        return self.__profile

    @profile.setter
    def profile(self, profile: str):
        self.__profile = profile

    @property
    def isrunnable(self) -> bool:
        return self.__isrunnable

    @isrunnable.setter
    def isrunnable(self, x: bool):
        self.__isrunnable = x

    @property
    def package(self):
        return self.__package

    @package.setter
    def package(self, _package_name: str):
        self.__package = _package_name

    @property
    def model_parameters(self) -> ModelParamTemplate:
        return self.__model_parameters
