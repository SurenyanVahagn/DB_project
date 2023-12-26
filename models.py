from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Adjust the connection string to your database
engine = create_engine('sqlite:///your-database-name.db', echo=True)

Base = declarative_base()

class Correspondent(Base):
    __tablename__ = 'correspondents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Float)
    country = Column(String)
    city = Column(String)
    # Assuming there's a one-to-many relationship between correspondents and events
    events = relationship('Event', back_populates='correspondent')

# Example of a generic 'Event' model
class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    duration = Column(Float)
    quality = Column(String)
    date = Column(Date)
    city = Column(String)
    danger_level = Column(String)
    event_type = Column(String)

# Example of a generic 'Reporter' model
class Reporter(Base):
    __tablename__ = 'reporters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Float)
    country = Column(String)
    city = Column(String)
    personal_id = Column(String)
    
    # Foreign Key to reference the 'Event' model
    event_id = Column(Integer, ForeignKey('events.id'))

# Create the tables in the database
Base.metadata.create_all(engine)

# Session creation to interact with the database
Session = sessionmaker(bind=engine)
session = Session()