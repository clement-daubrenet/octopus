from api.home.views import HomeHandler
from unittest.mock import patch, Mock


def test_get_most_common_words():
    """
    Testing the right behavior of get_most_common_words.
    """
    result = HomeHandler._get_most_common_words(['business',
                                                 'article',
                                                 'stuff',
                                                 'business',
                                                 'article'], 10)
    assert result == [('business', 2), ('article', 2), ('stuff', 1)]


def test_get_most_common_words_upper_case_lower_case():
    """
    Testing lower case/upper case mix up: they should be counted as the same
    word in lower case.
    """
    result = HomeHandler._get_most_common_words(['Business',
                                                 'business',
                                                 'bUsiness',
                                                 'busineSS'], 10)
    assert result == [('business', 4)]


def test_get_most_common_words_edge_case_1():
    """
    Testing 1 element scenario.
    :return:
    """
    result = HomeHandler._get_most_common_words(['business'], 10)
    assert result == [('business', 1)]


def test_get_most_common_words_edge_case_2():
    """
    Testing empty scenario.
    :return:
    """
    result = HomeHandler._get_most_common_words([], 10)
    assert result == []


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


def test_scale_frequencies_edge_case_1():
    """
    Testing the frequency scaling for the front-end.
    :return:
    """
    result = HomeHandler._scale_frequencies([('business', 15)])
    assert result == [('business', 10)]


def test_scale_frequencies_edge_case_2():
    """
    Testing the frequency scaling for the front-end.
    :return:
    """
    result = HomeHandler._scale_frequencies([])
    assert result == []


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
    word_id = Mock()
    new_count = 3
    HomeHandler._update_word(word_id, new_count)
    assert query_mock.called is True
    assert commit_mock.called is True
