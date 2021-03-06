from dictalchemy import DictableModel
from sqlalchemy.ext.declarative import declarative_base
from Crypto.PublicKey import RSA
import sqlalchemy
import pymysql
import os


Base = declarative_base(cls=DictableModel)

# Private key. On disk for now...
RSA_KEYFILE = os.path.join(os.path.dirname(__file__), 'key')
KEY = RSA.importKey(open(RSA_KEYFILE).read())

# Database for the API
pymysql.install_as_MySQLdb()
url = 'mysql://root:rootroot@database:3306/octopus'
engine = sqlalchemy.create_engine(url)
session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())
session.configure(bind=engine, autoflush=False, expire_on_commit=False)
