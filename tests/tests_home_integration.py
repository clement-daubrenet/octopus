from tornado.web import Application, url
from api.home.views import HomeHandler
from unittest.mock import patch
from tornado.testing import AsyncHTTPTestCase


def test_make_app():
    """
    A test make application for the integration tests.
    :return:
    """
    return Application([url(r'/', HomeHandler, name='home')])


class HomeIntegrationTests(AsyncHTTPTestCase):
    """
    Testing that the main functions are called (integration tests).
    """
    def get_app(self):
        """
        Getting the test application.
        :return:
        """
        return test_make_app()

    def get_url(self, path):
        """Returns an absolute url for the given path on the test server."""
        return '%s://localhost:%s%s' % (self.get_protocol(),
                                        self.get_http_port(), path)

    @patch('api.home.views.RequestHandler.render')
    def test_get_with_url(self, render_mock):
        """
        Testing that the get function is rendering when an URL is passed.
        :param render_mock: mock of the rendering method.
        :return:
        """
        self.fetch('/?url=https%3A%2F%2Fwww.bbc.co.uk%2Fnews%2Fbusiness&_xsrf'
                   '=2%7Cd22a942b%7C102fedc2faeaa2f0a04e71aeec5b754d%7C'
                   '1537801354', method="GET")
        assert render_mock.called is True

    @patch('api.home.views.RequestHandler.render')
    def test_get_without_url(self, render_mock):
        """
        Testing that the get function is rendering when no URL is passed.
        :return:
        """
        self.fetch('/', method="GET")
        assert render_mock.called is True



