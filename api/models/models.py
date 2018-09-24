from sqlalchemy import String, LargeBinary, Column, DateTime, Integer
from .. import Base, KEY
from datetime import datetime
from Crypto.Cipher import PKCS1_OAEP


class Word(Base):

    __tablename__ = 'words'

    id = Column(String(255), primary_key=True)
    word = Column(LargeBinary(), nullable=False)
    count = Column(Integer, nullable=False)
    modified = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, word_id, word, count):
        self.id = word_id
        self.word = self._encode_rsa(word)
        self.count = count

    @staticmethod
    def _encode_rsa(word):
        """
        Encode the word with the private key.
        :param word: the word to encrypt.
        :return:
        """
        cipher = PKCS1_OAEP.new(KEY)
        return cipher.encrypt(word.encode('utf-8'))

    def _decode_rsa(self):
        """
        Decode the word with the private key.
        :return:
        """
        cipher = PKCS1_OAEP.new(KEY)
        return cipher.decrypt(self.word)

    @property
    def decoded(self):
        """
        To access the decoded version of the word.
        :return:
        """
        return self._decode_rsa()
