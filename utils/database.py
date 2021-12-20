from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from data import config


class ConnectDB:
    def __init__(self):
        super(ConnectDB, self).__init__()
        self.engine = create_engine(config.sqlite_url)
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()
        self.session = self.Session()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)


db = ConnectDB()


class Cities(db.Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    weather = relationship('Statistic', backref='cities')


class Statistic(db.Base):
    __tablename__ = 'statistic'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date = Column(Date)
    temp = Column(Float)
    pcp = Column(Float)
    clouds = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    wind_speed = Column(Float)
