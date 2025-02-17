from datetime import datetime, timedelta
import streamlit as st
from models import Client, Agent, BookingIssue, Appointment
from database import get_db_session
from sqlalchemy import and_

# Initialize data directory - this part is no longer needed with the database
#if not os.path.exists('data'):
#    os.makedirs('data')

# Data file paths - these are no longer needed
#CLIENTS_FILE = 'data/clients.csv'
#AGENTS_FILE = 'data/agents.csv'
#BOOKING_ISSUES_FILE = 'data/booking_issues.csv'
#APPOINTMENTS_FILE = 'data/appointments.csv'

# load_data and save_data functions are no longer needed.

def get_active_clients():
    db = get_db_session()
    clients = db.query(Client.client_name).filter(Client.status == 'active').all()
    return [client[0] for client in clients]

def get_active_agents():
    db = get_db_session()
    agents = db.query(Agent.name).filter(Agent.status == 'active').all()
    return [agent[0] for agent in agents]

def calculate_appointments_by_date_range(start_date, end_date, client=None):
    db = get_db_session()
    query = db.query(Appointment)

    # Convert dates to datetime if they're not already
    start_dt = start_date if isinstance(start_date, datetime) else datetime.combine(start_date, datetime.min.time())
    end_dt = end_date if isinstance(end_date, datetime) else datetime.combine(end_date, datetime.max.time())

    query = query.filter(and_(
        Appointment.date >= start_dt,
        Appointment.date <= end_dt
    ))

    if client:
        query = query.filter(Appointment.client == client)

    return query.count()

def get_date_ranges():
    today = datetime.now().date()
    return {
        'Today': (today, today),
        'Last 7 Days': (today - timedelta(days=7), today),
        'This Month': (today.replace(day=1), today),
        'This Year': (today.replace(month=1, day=1), today)
    }