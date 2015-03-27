from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    """ this Class describes the kind User, to store GitHub tokens """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    github_access_token = Column(String(200))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token


class Restaurant(Base):
    """ this Class describes the kind Restaurant """
    #
    # Table
    #
    __tablename__ = 'restaurant'

    #
    # Mapper
    #
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class MenuItem(Base):
    """ this Class describes the kind MenuItem """
    #
    # Table
    #
    __tablename__ = 'menu_item'

    #
    # Mapper
    #
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
            'restaurant': self.restaurant.id
        }


def create_sqlite_file(eng):
    """Create and sql lite file"""
    Base.metadata.create_all(eng)


def start_session(eng):
    """This method starts an SQLAlchemy session"""
    Base.metadata.bind = eng
    DBSession = sessionmaker(bind=eng)
    session = DBSession()
    return session

# Start engine and create the local file to store the database
engine = create_engine(
    r'sqlite:///C:\Github\restaurantmenu.db'
)


