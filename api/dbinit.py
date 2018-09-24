from sqlalchemy import String, LargeBinary, Column, DateTime, Integer
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

import pymysql

Base = declarative_base()


class Word(Base):

    __tablename__ = 'words'

    id = Column(String(255), primary_key=True)
    word = Column(LargeBinary(), nullable=False)
    count = Column(Integer, nullable=False)
    modified = Column(DateTime, nullable=False, default=datetime.now())


if __name__ == '__main__':
    pymysql.install_as_MySQLdb()
    url = 'postgresql+psycopg2://user:pass@01.02.03.04/my_db'
    url = 'mysql://root:rootroot@localhost:3306/octopus'
    engine = sqlalchemy.create_engine(url)
    session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    Word.__table__.drop(session.bind)
    print('here')
    Word.__table__.create(session.bind)
