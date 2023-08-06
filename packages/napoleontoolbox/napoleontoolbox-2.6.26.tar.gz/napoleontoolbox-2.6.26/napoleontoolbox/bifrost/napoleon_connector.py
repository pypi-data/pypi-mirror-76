__author__ = "hugo.inzirillo"

import requests

from napoleontoolbox.bifrost import Scope
from napoleontoolbox.bifrost.headers import AuthenticationManager, AuthorizationHeaderManager, \
    TemplateConnectorManager, TemplateConnector
from napoleontoolbox.bifrost.utils.auth_handler import NapoleonServiceAuthHandler
from napoleontoolbox.bifrost.utils.rest_template import Post, Get
from napoleontoolbox.dataloader.models import NapoleonService
from napoleontoolbox.napoleon_config_tools import getter


class NapoleonAuthenticationManager(AuthenticationManager):

    @property
    @getter(value="providers.napoleon_service.access_token_uri")
    def url(self):
        return self.url

    @property
    def credentials(self):
        return NapoleonService().get_credentials()

    @property
    def scope(self):
        return Scope(["READ", "WRITE"])

    def _handle_reponse(self):
        if self.response:
            if self.response.status_code == requests.codes.OK:
                _reponse = self.response.json()
                self.token = NapoleonServiceAuthHandler(_reponse).get_token()
                self.authorization_header = AuthorizationHeaderManager(self.token).build()


class NapoleonConnectorManager(TemplateConnectorManager):
    def __init__(self):
        self.__authentication_manager = NapoleonAuthenticationManager()

    @property
    def authentication_manager(self):
        return self.__authentication_manager


class NapoleonPositionServiceConnector(TemplateConnector):
    def __init__(self):
        self.__connector_manager = NapoleonConnectorManager()

    @property
    def connector_manager(self):
        return self.__connector_manager

    def authenticate(self):
        return self.connector_manager.authentication_manager().authenticate()

    @Post("Test")
    def get_signal(self, **kwargs):
        """

        Parameters
        ----------
        kwargs

        Returns
        -------

        """
        pass


class Connector(object):
    def __init__(self):
        self.__hello = "Hugo"

    @property
    def hello(self):
        return self.__hello

    @Get("https://www.bitmex.com/api/v1/orderBook/L2?symbol={symbol}&depth={depth}")
    def get_order_book_l2(self, symbol: str = None, depth: int = None):
        """

        Parameters
        ----------
        kwargs

        Returns
        -------

        """
        pass


if __name__ == '__main__':
    a = Connector().get_order_book_l2(symbol="xbt", depth=100000)
