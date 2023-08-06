__author__ = "hugo.inzirillo"

from npxlogger.logger_manager import NapoleonLoggerManager

__all__ = ['log']
__version__ = "0.0.1"

log = NapoleonLoggerManager().get_logger(__package__)
########################## EXEMPLE ######################


# from npxlogger import log
# log.info()
# log.warning()
# log.error()
# log.warn()
