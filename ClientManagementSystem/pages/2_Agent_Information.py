import streamlit as st
import pandas as pd
from models import Agent
from database import get_db_session
from datetime import datetime

st.title("Agent Information")

# Initialize database session
db = get_db_session()

# Agent management form
with st.form("agent_form"):
    st.subheader("Add/Edit Agent")

    name = st.text_input("Name")
    location = st.text_input("Location")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    schedule = st.text_input("Schedule", placeholder="e.g., Mon-Fri 9AM-5PM")
    shift = st.selectbox("Shift", ["Morning", "Afternoon", "Evening"])
    notes = st.text_area("Notes")
    dob = st.date_input("Date of Birth")
    status = st.selectbox("Status", ["active", "paused", "inactive"])

    submitted = st.form_submit_button("Save Agent")

    if submitted and name:  # Ensure name is provided
        try:
            agent = db.query(Agent).filter(Agent.name == name).first()

            if agent:
                # Update existing agent
                agent.location = location
                agent.phone_number = phone
                agent.email = email
                agent.schedule = schedule
                agent.shift = shift
                agent.notes = notes
                agent.dob = dob
                agent.status = status
                message = "Agent updated successfully!"
            else:
                # Create new agent
                new_agent = Agent(
                    name=name,
                    location=location,
                    phone_number=phone,
                    email=email,
                    schedule=schedule,
                    shift=shift,
                    notes=notes,
                    dob=dob,
                    status=status
                )
                db.add(new_agent)
                message = "New agent created successfully!"

            db.commit()
            st.success(message)
        except Exception as e:
            st.error(f"Error saving agent: {str(e)}")
    elif submitted:
        st.error("Please provide a name for the agent")

# Display agents with color-coding and delete option
st.subheader("Agent List")
agents = db.query(Agent).order_by(Agent.name).all()

if agents:
    agents_data = []
    for a in agents:
        # Define color based on status
        if a.status == 'active':
            color = '#90EE90'  # Light green
        elif a.status == 'paused':
            color = '#FFB366'  # Light orange
        else:
            color = '#FF9999'  # Light red

        agents_data.append({
            'Name': a.name,
            'Location': a.location,
            'Phone': a.phone_number,
            'Email': a.email,
            'Schedule': a.schedule,
            'Shift': a.shift,
            'Status': a.status
        })

    df = pd.DataFrame(agents_data)

    # Apply color coding to the entire row based on status
    def highlight_rows(row):
        color = '#90EE90' if row['Status'] == 'active' else '#FFB366' if row['Status'] == 'paused' else '#FF9999'
        return [f'background-color: {color}'] * len(row)

    st.dataframe(
        df.style.apply(highlight_rows, axis=1),
        use_container_width=True
    )

    # Add delete option
    st.subheader("Delete Agent")
    agent_to_delete = st.selectbox("Select agent to delete", [a.name for a in agents])
    if st.button("Delete Agent"):
        if st.warning(f"Are you sure you want to delete {agent_to_delete}?"):
            try:
                agent = db.query(Agent).filter(Agent.name == agent_to_delete).first()
                if agent:
                    db.delete(agent)
                    db.commit()
                    st.success(f"Agent {agent_to_delete} has been deleted")
                    st.experimental_rerun()
            except Exception as e:
                st.error(f"Error deleting agent: {str(e)}")
else:
    st.info("No agents found. Add your first agent using the form above.")