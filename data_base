from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger import log_event
from  settings_loader import get_processor_settings

settings = get_processor_settings()

def get_session():
    # Создание подключения к базе данных
    engine = create_engine(f"postgresql://{settings['sqlalchemy_username']}:{settings['sqlalchemy_password']}@{settings['sqlalchemy_hostname']}/{settings['sqlalchemy_databasename']}")
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


Base = declarative_base()
UUID = String(36)
class Product(Base):

    __tablename__ = 'product_table'
    id = Column(UUID,primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    amount = Column(Integer)


class Order(Base):

    __tablename__ = 'order_table'
    id = Column(UUID,primary_key=True)
    date = Column(Date)
    status = Column(String(30))

class OrderItem(Base):

    __tablename__ = 'order_item_table'
    id = Column(UUID,primary_key=True)
    order_id = Column(UUID)
    item_id = Column(UUID)
    amount = Column(Integer)
