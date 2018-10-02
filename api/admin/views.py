from api import session
from api.models.models import Word
from sqlalchemy import desc
from tornado.web import RequestHandler
from .services import Pagination


class AdminHandler(RequestHandler):
    """
    This class is in charge of handling the admin page.
    """
    def get(self):
        """
        Getting the admin page.
        :return:
        """
        ordered_words = session.query(Word)\
            .order_by(desc('count')).all()
        
        self.render('admin.html',
                    ordered_words=ordered_words)

