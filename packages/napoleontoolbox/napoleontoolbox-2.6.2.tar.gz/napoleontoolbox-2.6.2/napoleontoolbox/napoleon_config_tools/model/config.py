import json

from napoleontoolbox.napoleon_config_tools.model.modelparamtemplate import ModelParamTemplate


# todo make meta dict


class Config(object):
    def __init__(self):
        self.__profile = None
        self.__isrunnable = bool()
        self.__package = str()
        self.__model_parameters = ModelParamTemplate()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.__dict__())

    def __dict__(self):
        return dict(profile=self.__profile,
                    isrunnable=self.__isrunnable,
                    package=self.__package,
                    model_parameters=self.__model_parameters.__dict__())

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
