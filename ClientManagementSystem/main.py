import streamlit as st
from datetime import datetime, time
from models import Client, Agent, Appointment
from database import get_db_session
from sqlalchemy import func

# Page configuration with custom theme and logo
st.set_page_config(
    page_title="Elite Scale Digital - Business Management System",
    page_icon="attached_assets/Untitled design (13).png",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            display: flex;
            align-items: center;
            padding: 1rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .logo-img {
            width: 200px;
            margin-right: 20px;
        }
        .metric-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton>button {
            width: 100%;
            background-color: #1f77b4;
            color: white;
        }
        .quick-link {
            padding: 1rem;
            background-color: white;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .st-emotion-cache-16txtl3 {
            padding: 3rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header with logo
st.markdown("""
    <div class="main-header">
        <img src="attached_assets/Untitled design (13).png" class="logo-img">
        <div>
            <h1>Business Management System</h1>
            <p>Welcome to Elite Scale Digital's Business Management System</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize database session
db = get_db_session()

# Display summary metrics in a grid with improved styling
col1, col2, col3 = st.columns(3)

with col1:
    active_clients = db.query(func.count(Client.id)).filter(
        Client.status == 'active'
    ).scalar() or 0
    st.markdown("""
        <div class="metric-card">
            <h3>Active Clients</h3>
            <h2 style="color: #1f77b4;">{}</h2>
        </div>
    """.format(active_clients), unsafe_allow_html=True)

with col2:
    active_agents = db.query(func.count(Agent.id)).filter(
        Agent.status == 'active'
    ).scalar() or 0
    st.markdown("""
        <div class="metric-card">
            <h3>Active Agents</h3>
            <h2 style="color: #1f77b4;">{}</h2>
        </div>
    """.format(active_agents), unsafe_allow_html=True)

with col3:
    today = datetime.now().date()
    today_appointments = db.query(func.count(Appointment.id)).filter(
        Appointment.datetime >= datetime.combine(today, time.min),
        Appointment.datetime <= datetime.combine(today, time.max)
    ).scalar() or 0
    st.markdown("""
        <div class="metric-card">
            <h3>Today's Appointments</h3>
            <h2 style="color: #1f77b4;">{}</h2>
        </div>
    """.format(today_appointments), unsafe_allow_html=True)

# Quick Links with improved styling
st.subheader("Quick Links")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="quick-link">
            <h4>Client Management</h4>
            <p>🏢 Client Information - Manage client profiles and details</p>
            <p>📊 Sub-Account KPIs - Track client performance metrics</p>
        </div>
        <div class="quick-link">
            <h4>Agent Management</h4>
            <p>👥 Agent Information - Manage agent profiles and schedules</p>
            <p>📈 Appointment Setters Tracker - Monitor agent performance</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="quick-link">
            <h4>Appointment Management</h4>
            <p>📅 Daily Appointments - View and manage daily appointments</p>
            <p>❗ Booking Issues - Track and resolve booking related issues</p>
        </div>
        <div class="quick-link">
            <h4>Need Help?</h4>
            <p>Contact support for assistance with the system</p>
            <p>Email: support@elitescaledigital.com</p>
        </div>
    """, unsafe_allow_html=True)