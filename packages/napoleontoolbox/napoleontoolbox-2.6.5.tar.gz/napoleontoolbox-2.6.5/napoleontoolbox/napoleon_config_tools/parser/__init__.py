__author__ = "hugo.inzirillo"

from napoleontoolbox.napoleon_config_tools.parser.parsertemplate import NapoleonToolboxConfigParser
from npxlogger import log

config = NapoleonToolboxConfigParser().read().parse()
print("une fois")


def target(_value: str):
    """

    Parameters
    ----------
    _value : parameter in the config.yml file to target

    Returns
    -------
    dict : value containing the param in the config
    """
    def inner_function(function):
        def wrapper(*args, **kwargs):
            log.info("target value in config :  {value}".format(value=_value))
            kwargs = __get(_value)
            function(*args, **kwargs)

        return wrapper

    return inner_function


def __get(_value: str):
    """

    Parameters
    ----------
    _value : target value in config

    Returns
    -------
    dict : value inside the config.yml file

    """
    _schema = _value.split(".")
    _attr = _schema[0]
    _filtered_config = getattr(config, _attr)
    field = ""
    len_schema = len(_schema)

    if len_schema == 1:
        return {_attr: _filtered_config}
    else:

        for iter in range(1, len(_schema)):
            _field = _schema[iter]
            if _field in _filtered_config:
                _filtered_config = _filtered_config[_field]
                field = _field
            else:
                log.error("missing {field} in config".format(field=field))
        return {field: _filtered_config}
