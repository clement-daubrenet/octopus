from tornado.web import Application, url
from api.admin.views import AdminHandler
from unittest.mock import patch
from tornado.testing import AsyncHTTPTestCase


def test_make_app():
    """
    A test make application for the integration tests.
    :return:
    """
    return Application([url(r'/admin', AdminHandler, name='admin')])


class AdminIntegrationTests(AsyncHTTPTestCase):
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

    @patch('api.admin.views.RequestHandler.render')
    def test_get(self, render_mock):
        """
        Testing that the admin rendering is called.
        :param render_mock: mock of the rendering method.
        :return:
        """
        self.fetch('/admin', method="GET")
        assert render_mock.called is True
