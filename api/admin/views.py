import tornado
from api import session
from api.models.models import Word
from sqlalchemy import desc
from tornado.web import RequestHandler


class AdminHandler(RequestHandler):
    """
    This class is in charge of handling the
    """
    def get(self):
        """
        :return:
        """
        ordered_words = session.query(Word).order_by(desc('count')).all()
        # TODO: Pagination
        self.render('admin.html', ordered_words=ordered_words)
