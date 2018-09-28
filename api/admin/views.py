from api import session
from api.models.models import Word
from sqlalchemy import desc
from tornado.web import RequestHandler
from .services import Pagination


class AdminHandler(RequestHandler):
    """
    This class is in charge of handling the admin page.
    """
    def get(self, per_page=10):
        """
        Getting the admin page.
        :param per_page: the number of items per page.
        :return:
        """
        page = self.get_argument("page", 1)
        count = session.query(Word).count()

        ordered_words = \
            session.query(Word).order_by(desc('count'))\
            .limit(per_page).offset((page - 1) * per_page)

        pagination = Pagination(page, per_page, count)
        self.render('admin.html',
                    ordered_words=ordered_words,
                    pagination=pagination)
