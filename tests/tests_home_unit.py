from api.home.views import HomeHandler
from unittest.mock import patch
import uuid


def test_get_most_common_words_empty():
    """
    Testing empty scenario.
    :return:
    """
    result = HomeHandler._get_most_common_words([],10)
    assert result == []


def test_get_most_common_words_regular():
    """
    Testing the right behavior of get_most_common_words.
    """
    result = HomeHandler._get_most_common_words(['business', 'article'], 10)
    assert result == [('business', 1), ('article', 1)]


def test_scale_frequencies():
    """
    Testing the frequency scaling for the front-end.
    :return:
    """
    result = HomeHandler._scale_frequencies([('business', 15), ('sport', 12),
                                             ('technology', 8), ('others', 1)])
    assert result == [('business', 10),
                      ('sport', 8),
                      ('technology', 6),
                      ('others', 1)]


@patch('api.home.views.session.add')
@patch('api.home.views.session.commit')
def test_add_word(add_mock, commit_mock):
    """
    Testing add word method.
    :param add_mock: A database "add" operation mock
    :param commit_mock: A database "commit" operation mock
    :return:
    """
    HomeHandler._add_word(('test_word', 1))
    assert add_mock.called is True
    assert commit_mock.called is True


@patch('api.home.views.session.query')
@patch('api.home.views.session.commit')
def test_update_word(query_mock, commit_mock):
    """
    Testing update word method.
    :param query_mock: A database "query" operation mock
    :param commit_mock: A database "commit" operation mock
    :return:
    """
    word_id = uuid.uuid4()
    new_count = 3
    HomeHandler._update_word(word_id, new_count)
    assert query_mock.called is True
    assert commit_mock.called is True
