import os

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def connection_string():
    return 'postgresql+psycopg2://%s:%s@postgres:%s/%s' % (
        os.environ.get('SQL_USER'), os.environ.get('SQL_PASSWORD'),
        os.environ.get('SQL_PORT'), os.environ.get('SQL_DATABASE'))


Base = declarative_base()


class Product(Base):
    __tablename__ = 'src_product'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)

    engine = None
    Session = None
    session = None

    @staticmethod
    def insert(title, category, uniq_id):
        if Product.engine is None:
            conn_string = connection_string()
            print(conn_string)

            Product.engine = create_engine(conn_string)

            Product.Session = sessionmaker(bind=Product.engine)
            Product.session = Product.Session()

        exists = Product.session.query(Product.id).filter_by(id=id) is not None
        if exists:
            return

        cur_id = abs(hash(uniq_id)) % (10 ** 8)

        prod = Product(title=title, category=category, id=cur_id)

        Product.session.add(prod)

    @staticmethod
    def commit():
        Product.session.commit()
