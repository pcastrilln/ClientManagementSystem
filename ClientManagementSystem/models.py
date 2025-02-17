from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, unique=True, index=True)
    contact_name = Column(String)
    contact_method = Column(String)
    trial_model = Column(String)
    start_trial = Column(Date)
    expected_trial_end = Column(Date)
    actual_trial_end = Column(Date)
    official_start_date = Column(Date)
    guarantee_met = Column(Boolean)
    continued_after_trial = Column(Boolean)
    booking_login_link = Column(String)
    user = Column(String)
    password = Column(String)
    google_reviews_link = Column(String)
    website_link = Column(String)
    instagram_link = Column(String)
    cherry_link = Column(String)
    before_after_pictures = Column(Text)
    status = Column(String)  # active, paused, inactive

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    phone_number = Column(String)
    email = Column(String)
    schedule = Column(String)
    shift = Column(String)
    notes = Column(Text)
    dob = Column(Date)
    status = Column(String)  # active, paused, inactive

class BookingIssue(Base):
    __tablename__ = "booking_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    account = Column(String, ForeignKey("clients.client_name"))
    issue = Column(String)  # availability, price, other
    reporting_rep = Column(String, ForeignKey("agents.name"))
    lead_name = Column(String)
    lead_phone_number = Column(String)
    to_do = Column(Text)

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime)  # Changed from date to datetime
    client = Column(String, ForeignKey("clients.client_name"))
    setter = Column(String, ForeignKey("agents.name"))
    notes = Column(Text)

# Create the database tables
Base.metadata.create_all(bind=engine)