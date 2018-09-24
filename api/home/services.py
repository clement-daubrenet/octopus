from bs4 import BeautifulSoup, Comment


def is_not_code(element):
    """
    Returns True if it's an actual word of the web page
    (and not a code-related one).
    :param element: element from the Beautiful soup parsing.
    :return:
    """
    if element.parent.name in ['style',
                               'script',
                               'head',
                               'title',
                               'meta',
                               '[document]'] or isinstance(element, Comment):
        return False
    return True
