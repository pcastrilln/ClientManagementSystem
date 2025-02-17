import streamlit as st
import pandas as pd
from datetime import datetime
from models import BookingIssue, Client
from database import get_db_session
from utils import get_active_clients, get_active_agents

st.title("Booking Issues")

# Initialize database session
db = get_db_session()

# Booking issues form
with st.form("booking_issues_form"):
    st.subheader("Add Booking Issue")

    date = st.date_input("Date")
    account = st.selectbox("Account", get_active_clients())
    issue = st.selectbox("Issue", ["availability", "price", "other"])
    reporting_rep = st.selectbox("Reporting Rep", get_active_agents())
    lead_name = st.text_input("Lead Name")
    lead_phone = st.text_input("Lead Phone Number")
    to_do = st.text_area("To Do")

    submitted = st.form_submit_button("Save Issue")

    if submitted:
        new_issue = BookingIssue(
            date=date,
            account=account,
            issue=issue,
            reporting_rep=reporting_rep,
            lead_name=lead_name,
            lead_phone_number=lead_phone,
            to_do=to_do
        )

        db.add(new_issue)
        db.commit()
        st.success("Booking issue saved successfully!")

# Display issues with filtering
st.subheader("Booking Issues List")

# Get all clients for filter
all_clients = [client[0] for client in db.query(Client.client_name).distinct()]
selected_client = st.selectbox("Filter by Client", ["All Clients"] + all_clients)

# Query issues with filter
query = db.query(BookingIssue).order_by(BookingIssue.date.desc())
if selected_client != "All Clients":
    query = query.filter(BookingIssue.account == selected_client)

issues = query.all()

if issues:
    issues_data = [{
        'Date': i.date,
        'Account': i.account,
        'Issue': i.issue,
        'Reporting Rep': i.reporting_rep,
        'Lead Name': i.lead_name,
        'Phone': i.lead_phone_number,
        'To Do': i.to_do
    } for i in issues]

    df = pd.DataFrame(issues_data)

    # Add download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Issues List",
        data=csv,
        file_name=f"booking_issues_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    st.dataframe(df, use_container_width=True)
else:
    st.info("No booking issues found.")