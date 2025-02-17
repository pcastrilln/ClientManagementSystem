import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
from models import Appointment, Client
from database import get_db_session
from utils import get_date_ranges
from sqlalchemy import func

st.title("Sub-Account KPIs")

# Initialize database session
db = get_db_session()

# Get all clients, not just active ones
clients = db.query(Client).all()

if clients:
    # Create columns for different date ranges
    st.subheader("Client Performance Overview")

    # Calculate date ranges
    today = datetime.now().date()
    week_start = today - timedelta(days=7)
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    # Prepare data for all clients
    clients_data = []
    for client in clients:
        # Get appointments for different time periods
        today_appts = db.query(func.count(Appointment.id)).filter(
            Appointment.client == client.client_name,
            Appointment.datetime >= datetime.combine(today, time.min),
            Appointment.datetime <= datetime.combine(today, time.max)
        ).scalar() or 0

        week_appts = db.query(func.count(Appointment.id)).filter(
            Appointment.client == client.client_name,
            Appointment.datetime >= datetime.combine(week_start, time.min),
            Appointment.datetime <= datetime.combine(today, time.max)
        ).scalar() or 0

        month_appts = db.query(func.count(Appointment.id)).filter(
            Appointment.client == client.client_name,
            Appointment.datetime >= datetime.combine(month_start, time.min),
            Appointment.datetime <= datetime.combine(today, time.max)
        ).scalar() or 0

        year_appts = db.query(func.count(Appointment.id)).filter(
            Appointment.client == client.client_name,
            Appointment.datetime >= datetime.combine(year_start, time.min),
            Appointment.datetime <= datetime.combine(today, time.max)
        ).scalar() or 0

        clients_data.append({
            'Client': client.client_name,
            'Status': client.status,
            "Today's Appointments": today_appts,
            'Last 7 Days': week_appts,
            'This Month': month_appts,
            'This Year': year_appts
        })

    # Create DataFrame
    df = pd.DataFrame(clients_data)

    # Apply color coding based on status
    def highlight_rows(row):
        color = '#90EE90' if row['Status'] == 'active' else '#FFB366' if row['Status'] == 'paused' else '#FF9999'
        return [f'background-color: {color}'] * len(row)

    # Display the styled DataFrame
    st.dataframe(
        df.style.apply(highlight_rows, axis=1),
        use_container_width=True
    )

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Today", sum(d["Today's Appointments"] for d in clients_data))
    with col2:
        st.metric("Total Last 7 Days", sum(d['Last 7 Days'] for d in clients_data))
    with col3:
        st.metric("Total This Month", sum(d['This Month'] for d in clients_data))
    with col4:
        st.metric("Total This Year", sum(d['This Year'] for d in clients_data))

    # Custom date range search
    st.subheader("Custom Date Range Search")
    col1, col2 = st.columns(2)
    with col1:
        custom_start = st.date_input("Start Date", key="custom_start")
    with col2:
        custom_end = st.date_input("End Date", key="custom_end")

    if st.button("Search"):
        custom_data = []
        for client in clients:
            appointments = db.query(func.count(Appointment.id)).filter(
                Appointment.client == client.client_name,
                Appointment.datetime >= datetime.combine(custom_start, time.min),
                Appointment.datetime <= datetime.combine(custom_end, time.max)
            ).scalar() or 0

            custom_data.append({
                'Client': client.client_name,
                'Status': client.status,
                'Appointments': appointments
            })

        custom_df = pd.DataFrame(custom_data)
        st.subheader(f"Appointments from {custom_start} to {custom_end}")
        st.dataframe(
            custom_df.style.apply(highlight_rows, axis=1),
            use_container_width=True
        )
else:
    st.info("No clients found in the database.")