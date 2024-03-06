from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    cloudiness = Column(Float)
    date = Column(Date)
