import streamlit as st
from datetime import datetime, timedelta
from models import Client, Appointment
from database import get_db_session
from sqlalchemy import func
import pandas as pd

st.title("Client Information")

# Initialize database session
db = get_db_session()

# Client search and edit section
st.subheader("Search and Edit Client")
all_clients = db.query(Client).all()
client_names = [c.client_name for c in all_clients]
selected_client_name = st.selectbox("Select Client to Edit", [""] + client_names)

if selected_client_name:
    client = db.query(Client).filter(Client.client_name == selected_client_name).first()

    with st.form("client_edit_form"):
        st.subheader(f"Edit {selected_client_name}")

        contact_name = st.text_input("Contact Name", value=client.contact_name)
        contact_method = st.text_input("Contact Method", value=client.contact_method)
        trial_model = st.text_input("Trial Account/Deposit Model", value=client.trial_model)

        col1, col2 = st.columns(2)
        with col1:
            start_trial = st.date_input("Start Trial", value=client.start_trial)
            expected_trial_end = st.date_input("Expected Trial End", value=client.expected_trial_end)
        with col2:
            actual_trial_end = st.date_input("Actual Trial End", value=client.actual_trial_end)
            official_start = st.date_input("Official Starting Date", value=client.official_start_date)

        guarantee_met = st.selectbox("Guarantee Met?", ["Yes", "No"], index=0 if client.guarantee_met else 1)
        continued_trial = st.selectbox("Continued After Trial?", ["Yes", "No"], index=0 if client.continued_after_trial else 1)

        col3, col4 = st.columns(2)
        with col3:
            booking_link = st.text_input("Booking Login Link", value=client.booking_login_link)
            user = st.text_input("User", value=client.user)
            password = st.text_input("Password", value=client.password, type="password")

        with col4:
            google_link = st.text_input("Google Reviews Link", value=client.google_reviews_link)
            website_link = st.text_input("Website Link", value=client.website_link)
            instagram_link = st.text_input("Instagram Link", value=client.instagram_link)
            cherry_link = st.text_input("Cherry Link", value=client.cherry_link)

        pictures = st.text_area("Before and After Pictures (URLs)", value=client.before_after_pictures)
        status = st.selectbox("Status", ["active", "paused", "inactive"], index=["active", "paused", "inactive"].index(client.status))

        submitted = st.form_submit_button("Update Client")

        if submitted:
            client.contact_name = contact_name
            client.contact_method = contact_method
            client.trial_model = trial_model
            client.start_trial = start_trial
            client.expected_trial_end = expected_trial_end
            client.actual_trial_end = actual_trial_end
            client.official_start_date = official_start
            client.guarantee_met = (guarantee_met == "Yes")
            client.continued_after_trial = (continued_trial == "Yes")
            client.booking_login_link = booking_link
            client.user = user
            client.password = password
            client.google_reviews_link = google_link
            client.website_link = website_link
            client.instagram_link = instagram_link
            client.cherry_link = cherry_link
            client.before_after_pictures = pictures
            client.status = status

            db.commit()
            st.success("Client updated successfully!")

# Add new client form 
st.subheader("Add New Client")
with st.form("client_form"):
    client_name = st.text_input("Client Name")
    contact_name = st.text_input("Contact Name")
    contact_method = st.text_input("Contact Method")
    trial_model = st.text_input("Trial Account/Deposit Model")

    col1, col2 = st.columns(2)
    with col1:
        start_trial = st.date_input("Start Trial")
        expected_trial_end = st.date_input("Expected Trial End")
    with col2:
        actual_trial_end = st.date_input("Actual Trial End")
        official_start = st.date_input("Official Starting Date")

    guarantee_met = st.selectbox("Guarantee Met?", ["Yes", "No"])
    continued_trial = st.selectbox("Continued After Trial?", ["Yes", "No"])

    col3, col4 = st.columns(2)
    with col3:
        booking_link = st.text_input("Booking Login Link")
        user = st.text_input("User")
        password = st.text_input("Password", type="password")

    with col4:
        google_link = st.text_input("Google Reviews Link")
        website_link = st.text_input("Website Link")
        instagram_link = st.text_input("Instagram Link")
        cherry_link = st.text_input("Cherry Link")

    pictures = st.text_area("Before and After Pictures (URLs)")
    status = st.selectbox("Status", ["active", "paused", "inactive"])

    submitted = st.form_submit_button("Save Client")

    if submitted:
        client = db.query(Client).filter(Client.client_name == client_name).first()

        if client:
            # Update existing client
            client.contact_name = contact_name
            client.contact_method = contact_method
            client.trial_model = trial_model
            client.start_trial = start_trial
            client.expected_trial_end = expected_trial_end
            client.actual_trial_end = actual_trial_end
            client.official_start_date = official_start
            client.guarantee_met = (guarantee_met == "Yes")
            client.continued_after_trial = (continued_trial == "Yes")
            client.booking_login_link = booking_link
            client.user = user
            client.password = password
            client.google_reviews_link = google_link
            client.website_link = website_link
            client.instagram_link = instagram_link
            client.cherry_link = cherry_link
            client.before_after_pictures = pictures
            client.status = status
        else:
            # Create new client
            new_client = Client(
                client_name=client_name,
                contact_name=contact_name,
                contact_method=contact_method,
                trial_model=trial_model,
                start_trial=start_trial,
                expected_trial_end=expected_trial_end,
                actual_trial_end=actual_trial_end,
                official_start_date=official_start,
                guarantee_met=(guarantee_met == "Yes"),
                continued_after_trial=(continued_trial == "Yes"),
                booking_login_link=booking_link,
                user=user,
                password=password,
                google_reviews_link=google_link,
                website_link=website_link,
                instagram_link=instagram_link,
                cherry_link=cherry_link,
                before_after_pictures=pictures,
                status=status
            )
            db.add(new_client)

        db.commit()
        st.success("Client information saved successfully!")

# Display clients with filtering 
st.subheader("Client List and Statistics")

# Status filter
status_filter = st.multiselect(
    "Filter by Status",
    ["active", "paused", "inactive"],
    default=["active", "paused"]
)

# Date range filter
date_filter = st.selectbox(
    "Select Date Range",
    ["Today", "Last 7 Days", "This Month", "This Year"]
)

# Calculate date range
today = datetime.now().date()
if date_filter == "Today":
    start_date = today
    end_date = today
elif date_filter == "Last 7 Days":
    start_date = today - timedelta(days=7)
    end_date = today
elif date_filter == "This Month":
    start_date = today.replace(day=1)
    end_date = today
else:  # This Year
    start_date = today.replace(month=1, day=1)
    end_date = today

# Get clients with appointment counts
clients = db.query(Client).filter(Client.status.in_(status_filter)).all()
if clients:
    clients_data = []
    for c in clients:
        # Count appointments for the selected date range
        appointment_count = db.query(func.count(Appointment.id)).filter(
            Appointment.client == c.client_name,
            Appointment.datetime >= datetime.combine(start_date, datetime.min.time()),
            Appointment.datetime <= datetime.combine(end_date, datetime.max.time())
        ).scalar() or 0

        clients_data.append({
            'Client': c.client_name,
            'Contact Name': c.contact_name,
            'Status': c.status,
            'Trial Model': c.trial_model,
            f'Appointments ({date_filter})': appointment_count
        })

    # Create DataFrame and sort by appointment count
    df = pd.DataFrame(clients_data)
    df = df.sort_values(f'Appointments ({date_filter})', ascending=False)

    # Apply color coding based on status
    def highlight_rows(row):
        color = '#90EE90' if row['Status'] == 'active' else '#FFB366' if row['Status'] == 'paused' else '#FF9999'
        return [f'background-color: {color}'] * len(row)

    # Display statistics with color coding
    st.dataframe(
        df.style.apply(highlight_rows, axis=1),
        use_container_width=True
    )

    # Show total appointments
    total_appointments = sum(d[f'Appointments ({date_filter})'] for d in clients_data)
    st.metric(f"Total Appointments ({date_filter})", total_appointments)
    
    # Add download button for client list
    clients_df = pd.DataFrame(clients_data)
    csv = clients_df.to_csv(index=False)
    st.download_button(
        label="Download Client List",
        data=csv,
        file_name=f"clients_list_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

else:
    st.info("No clients found with the selected status.")