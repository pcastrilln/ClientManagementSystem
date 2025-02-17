import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta
from models import Appointment, Client # Added Client import
from database import get_db_session
from utils import get_active_clients, get_active_agents, get_date_ranges # Added get_date_ranges import

st.title("Daily Appointments")

# Custom CSS for better styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            width: 100%;
        }
        .appointment-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .filter-section {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize database session
db = get_db_session()

# Appointment form
with st.form("appointment_form"):
    st.markdown('<div class="appointment-card">', unsafe_allow_html=True)
    st.subheader("Add Appointment")

    date = st.date_input("Date")
    time_value = st.time_input("Time", value=time(9, 0))  # Default to 9:00 AM

    # Combine date and time
    datetime_value = datetime.combine(date, time_value)

    client = st.selectbox("Client", get_active_clients())
    setter = st.selectbox("Setter", get_active_agents())
    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Save Appointment")
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        new_appointment = Appointment(
            datetime=datetime_value,
            client=client,
            setter=setter,
            notes=notes
        )

        db.add(new_appointment)
        db.commit()
        st.success("Appointment saved successfully!")

# Display appointments with filtering
st.subheader("View Appointments")

# Filter section
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    # Client filter
    all_clients = ["All Clients"] + get_active_clients()
    selected_client = st.selectbox("Filter by Client", all_clients)

with col2:
    # Date range filter
    date_ranges = {
        'Today': (datetime.now().date(), datetime.now().date()),
        'Last 7 Days': (datetime.now().date() - timedelta(days=7), datetime.now().date()),
        'This Month': (datetime.now().date().replace(day=1), datetime.now().date()),
        'This Year': (datetime.now().date().replace(month=1, day=1), datetime.now().date()),
        'Custom Range': None
    }

    selected_range = st.selectbox("Select Date Range", list(date_ranges.keys()))

# Custom date range if selected
if selected_range == 'Custom Range':
    col3, col4 = st.columns(2)
    with col3:
        start_date = st.date_input("Start Date", datetime.now().date() - timedelta(days=7))
    with col4:
        end_date = st.date_input("End Date", datetime.now().date())
else:
    start_date, end_date = date_ranges[selected_range]

st.markdown('</div>', unsafe_allow_html=True)

# Query appointments with filters
query = db.query(Appointment).filter(
    Appointment.datetime >= datetime.combine(start_date, time.min),
    Appointment.datetime <= datetime.combine(end_date, time.max)
)

if selected_client != "All Clients":
    query = query.filter(Appointment.client == selected_client)

appointments = query.order_by(Appointment.datetime).all()

if appointments:
    appointments_data = [{
        'Date': a.datetime.strftime('%Y-%m-%d'),
        'Time': a.datetime.strftime('%I:%M %p'),
        'Client': a.client,
        'Setter': a.setter,
        'Notes': a.notes
    } for a in appointments]

    df = pd.DataFrame(appointments_data)

    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label=f"Download Appointments ({start_date} to {end_date})",
        data=csv,
        file_name=f"appointments_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

    # Display appointments with improved styling
    st.dataframe(
        df.style.set_properties(**{
            'background-color': '#f8f9fa',
            'color': '#262730',
            'border-color': '#dee2e6'
        }),
        use_container_width=True
    )
else:
    st.info("No appointments found for the selected filters.")