from tornado.web import RequestHandler, HTTPError
from bs4 import BeautifulSoup
from .services import is_not_code
from nltk.tokenize import wordpunct_tokenize
from collections import Counter
from nltk.corpus import stopwords
from api import session
from api.models.models import Word

import requests
import nltk
import math
import os
import hashlib


class HomeHandler(RequestHandler):
    """
    Class in charge of serving the home page where the word cloud generation
    takes place. The logic in it has been (heavily) inspired by different
    projects I found online: "Beautiful souping" the web page, get tagged
    tokens out of it and store/update the words.
    """

    def get(self):
        """
        The get request called when the home page is loaded.
        More details on the rendering system of tornado works:
        https://www.tornadoweb.org/en/stable/guide/templates.html
        :return:
        """

        if not self.get_argument("url", None):
            return self.render('home.html', url=None, most_common_words={})

        self.render('home.html',
                    url=self.get_argument("url", None),
                    most_common_words=self._get_words_distribution())

    def _get_words_distribution(self):
        """
        Getting a words distribution based on words occurrences on the page.
        n.b: We try to have a 0-10 scaled distribution sent to the front-end.
        I took this idea from another project to go faster.
        :return list scaled_words_distribution: A weighted words distribution.
        e.g: [('business', 10), ('article', 9), ('september', 8), ('video', 7),
        ('section', 4), ('news', 3), ('bbc', 3), ('world', 3), ('home', 2)]
        """
        tokens = self._parse_url()
        most_common_words = self._get_most_common_words(tokens)
        self._add_or_update_words(most_common_words)
        scaled_words_distribution = self._scale_frequencies(most_common_words)
        return scaled_words_distribution

    def _parse_url(self):
        """
        Parsing the web page to extract text tokens (individual words).
        n.b.1: The error handling is dealing with a broad range or errors: we
        don't want to go through them one by one. Using the Exception mother
        class and displaying the specific error message is more flexible.
        n.b.2: For more information on what "tokens" are in a language
        processing context, please check an helpful set of test cases:
        http://www.nltk.org/howto/tokenize.html
        :return list tokens: A list of words, extracted from the web page.
        e.g: ['homepage', 'accessibility', 'links', 'skip', 'to', 'content']
        """
        try:
            response = requests.get(url=self.get_argument("url"))
        except requests.exceptions.RequestException as error:
            error_message = 'Sorry, the word cloud generation could not ' \
                            'succeed because of the error: {}'.format(error)
            raise HTTPError(404, reason=error_message)

        beautiful_soup = BeautifulSoup(response.text, 'html.parser')
        texts = beautiful_soup.findAll(text=True)
        words = u" ".join(text.lower() for text in filter(is_not_code, texts))
        tokens = wordpunct_tokenize(words)
        return tokens

    @staticmethod
    def _get_most_common_words(tokens, maximum=100):
        """
        Getting the most top-[maximum] occurrences of words. We only keep
        nouns and verbs (based on their tags).
        n.b: warning, this is english only for now.
        :param list tokens: List of tokens coming from the parsing of the page.
        e.g: [('business', 50), ('article', 30) ... ('september', 2),
        ('section', 1), ('news', 1), ('bbc', 1), ('world', 1), ('home', 1)]
        :param integer maximum: the number of most common words.
        e.g: 100
        :return list most_common_words: The top-[maximum] words with their
        number of occurrences.
        e.g: [('business', 50), ('article', 30) ... ('technology', 10)]
        """
        words_counter = Counter()
        for word, post in nltk.pos_tag(tokens):
            if (post.startswith('NN') or post.startswith('VB'))\
                    and word not in stopwords.words("english") \
                    and len(word) > 1:
                words_counter[word] += 1
        return words_counter.most_common(maximum)

    def _add_or_update_words(self, most_common_words):
        """
        Adding or updating the words in the database depending on the case.
        n.b: I'm not proud of this one. Fetching the whole IDs because I
        could not fetch by encoded word. I just lack of time to improve it.
        :param list most_common_words: The top-[maximum] words with their
        number of occurrences.
        e.g: [('business', 50), ('article', 30) ... ('technology', 10)]
        :return:
        """
        database_words = \
            [(word.decoded, word.id) for word in session.query(Word).all()]

        for common_word in most_common_words:
            self._add_or_update_word(common_word, database_words)

    def _add_or_update_word(self, parsed_word, database_words):
        """
        Adding or updating a word count depending on its presence (or not)
        in the database.
        :param parsed_word: a parsed word and its count.
        e.g: ('business', 30)
        :param database_words: the words IDs and count in the current database.
        e.g: [(<id1>, 50), (<id2>, 30) ... (<id302>, 10)]
        :return:
        """
        try:
            database_word = \
                next(filter(lambda x: x[0] == parsed_word[0].encode(),
                            database_words))
            self._update_word(database_word[1], parsed_word[1])
        except (StopIteration, TypeError):
            self._add_word(parsed_word)

    @staticmethod
    def _add_word(word):
        """
        Adding a word in the database.
        :param tuple word: a parsed word and its count.
        e.g: ('business', 30)
        """
        word = \
            Word(
                word_id=
                hashlib.sha1(os.urandom(16) + word[0].encode()).hexdigest(),
                word=word[0],
                count=word[1])
        session.add(word)
        session.commit()

    @staticmethod
    def _update_word(word_id, new_count):
        """
        Update word with the new count.
        :param uuid word_id: A word primary key.
        :param int new_count: The new count of the word to add to the one in
        the database.
        """
        session.query(Word).filter(Word.id == word_id).\
            update({'count': (Word.count + new_count)})
        session.commit()

    @staticmethod
    def _scale_frequencies(most_common_words):
        """
        We want a frequency in the 0-10 spectrum for the display.
        :return:
        """
        return [(word, int(math.ceil(10 * wc/most_common_words[0][1])))
                for word, wc in most_common_words]
