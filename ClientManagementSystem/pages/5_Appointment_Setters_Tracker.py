import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
from models import Appointment, Agent, Client
from database import get_db_session
from sqlalchemy import func

st.title("Appointment Setters Tracker")

# Initialize database session
db = get_db_session()

# Get active agents
active_agents = db.query(Agent).filter(Agent.status == 'active').all()

if active_agents:
    # Calculate current day and month ranges
    today = datetime.now().date()
    current_month = today.month
    current_year = today.year
    month_start = datetime(current_year, current_month, 1).date()
    month_end = (datetime(current_year, current_month + 1, 1) - timedelta(days=1)).date() if current_month < 12 else datetime(current_year, 12, 31).date()

    # Get all clients for detailed view
    clients = db.query(Client).all()

    # Calculate performance metrics for today and current month
    performance_data = []
    detailed_data = []

    for agent in active_agents:
        # Today's appointments
        today_appointments = db.query(func.count(Appointment.id)).filter(
            Appointment.setter == agent.name,
            Appointment.datetime >= datetime.combine(today, time.min),
            Appointment.datetime <= datetime.combine(today, time.max)
        ).scalar() or 0

        # Month's appointments
        month_appointments = db.query(func.count(Appointment.id)).filter(
            Appointment.setter == agent.name,
            Appointment.datetime >= datetime.combine(month_start, time.min),
            Appointment.datetime <= datetime.combine(month_end, time.max)
        ).scalar() or 0

        performance_data.append({
            'Agent': agent.name,
            'Location': agent.location,
            'Shift': agent.shift,
            "Today's Appointments": today_appointments,
            f'Appointments for {month_start.strftime("%B %Y")}': month_appointments
        })

        # Get appointments by client for this agent
        for client in clients:
            client_today = db.query(func.count(Appointment.id)).filter(
                Appointment.setter == agent.name,
                Appointment.client == client.client_name,
                Appointment.datetime >= datetime.combine(today, time.min),
                Appointment.datetime <= datetime.combine(today, time.max)
            ).scalar() or 0

            client_month = db.query(func.count(Appointment.id)).filter(
                Appointment.setter == agent.name,
                Appointment.client == client.client_name,
                Appointment.datetime >= datetime.combine(month_start, time.min),
                Appointment.datetime <= datetime.combine(month_end, time.max)
            ).scalar() or 0

            if client_today > 0 or client_month > 0:
                detailed_data.append({
                    'Agent': agent.name,
                    'Client': client.client_name,
                    "Today's Appointments": client_today,
                    f'Appointments for {month_start.strftime("%B %Y")}': client_month
                })

    # Create and display performance DataFrame
    performance_df = pd.DataFrame(performance_data)

    # Display metrics
    st.subheader("Current Performance")

    # Add download button for performance data
    csv = performance_df.to_csv(index=False)
    st.download_button(
        label="Download Performance Report",
        data=csv,
        file_name=f"agent_performance_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    st.dataframe(performance_df, use_container_width=True)

    # Show total appointments
    col1, col2 = st.columns(2)
    with col1:
        total_today = sum(d["Today's Appointments"] for d in performance_data)
        st.metric("Total Appointments Today", total_today)
    with col2:
        total_month = sum(d[f'Appointments for {month_start.strftime("%B %Y")}'] for d in performance_data)
        st.metric(f"Total Appointments for {month_start.strftime('%B %Y')}", total_month)

    # Display detailed appointments by client
    st.subheader("Appointments by Agent and Client")
    if detailed_data:
        detailed_df = pd.DataFrame(detailed_data)

        # Add download button for detailed data
        detailed_csv = detailed_df.to_csv(index=False)
        st.download_button(
            label="Download Detailed Report",
            data=detailed_csv,
            file_name=f"agent_client_details_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        st.dataframe(detailed_df, use_container_width=True)
    else:
        st.info("No appointments found for the current period")

    # Visualization
    st.subheader("Appointments Distribution")

    # Today's appointments chart
    st.bar_chart(
        performance_df.set_index('Agent')["Today's Appointments"],
        use_container_width=True
    )

    # Custom date range search
    st.subheader("Custom Date Range Search")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

    if st.button("Search"):
        custom_data = []
        for agent in active_agents:
            appointments = db.query(func.count(Appointment.id)).filter(
                Appointment.setter == agent.name,
                Appointment.datetime >= datetime.combine(start_date, time.min),
                Appointment.datetime <= datetime.combine(end_date, time.max)
            ).scalar() or 0

            custom_data.append({
                'Agent': agent.name,
                'Appointments': appointments
            })

        custom_df = pd.DataFrame(custom_data)
        st.subheader(f"Appointments from {start_date} to {end_date}")

        # Add download button for custom date range
        custom_csv = custom_df.to_csv(index=False)
        st.download_button(
            label="Download Custom Range Report",
            data=custom_csv,
            file_name=f"custom_range_{start_date}_{end_date}.csv",
            mime="text/csv"
        )

        st.dataframe(custom_df, use_container_width=True)
        st.bar_chart(custom_df.set_index('Agent')['Appointments'])

else:
    st.warning("No active agents found. Please add agents and set their status to active.")