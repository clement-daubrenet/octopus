from tornado.web import url, Application
from api.home.views import HomeHandler
from api.admin.views import AdminHandler
from settings import TEMPLATE_PATH, STATIC_PATH
import tornado


def make_app():
    settings = {
        "template_path": TEMPLATE_PATH,
        "static_path": STATIC_PATH,
    }
    return Application([url(r'/', HomeHandler, name='home'),
                        url(r'/admin', AdminHandler, name='admin')],
                       **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


