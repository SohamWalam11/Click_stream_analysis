import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os
import csv

# Constants
TRACKING_FILE = os.path.join("data", "tracking.csv")

# Main Page
def main():
    st.title("Clickstream Tracking Dashboard")

    # Home page
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Home", "About", "Products", "Dashboard", "Simulate Tracking"))

    if page == "Home":
        st.header("Welcome to the Clickstream Tracking System")
        st.write("This app tracks user activity across different pages.")
    elif page == "About":
        st.header("About")
        st.write("This app tracks user behavior and provides insights like total clicks, average time spent per page, etc.")
    elif page == "Products":
        st.header("Products")
        st.write("Here you can view products and their details.")
    elif page == "Dashboard":
        dashboard()
    elif page == "Simulate Tracking":
        simulate_tracking()

# Dashboard Page
def dashboard():
    if not os.path.isfile(TRACKING_FILE):
        st.warning("No data available.")
        return

    df = pd.read_csv(TRACKING_FILE)
    
    if df.empty:
        st.warning("No data available.")
        return

    # Normalize and check required columns
    df.columns = df.columns.str.strip()
    df['Page'] = df['Page'].str.lower().str.strip()

    required_columns = {'Page', 'Clicks', 'Avg Time Spent'}
    if not required_columns.issubset(df.columns):
        st.error("Missing required columns in tracking.csv")
        return

    # Grouping for summary
    summary = df.groupby('Page').agg({
        'Clicks': 'sum',
        'Avg Time Spent': 'mean'
    }).reset_index()

    # Visualizations
    st.subheader("📊 Clicks per Page")
    bar_fig = px.bar(summary, x='Page', y='Clicks', title='Clicks per Page', color='Page')
    st.plotly_chart(bar_fig)

    st.subheader("📈 Click Distribution by Page")
    pie_fig = px.pie(summary, names='Page', values='Clicks', title='Click Distribution by Page')
    st.plotly_chart(pie_fig)

    st.subheader("⏱️ Average Time Spent per Page (s)")
    time_fig = px.bar(summary, x='Page', y='Avg Time Spent', title='Average Time Spent per Page', color='Page')
    st.plotly_chart(time_fig)

    # Show raw data if needed
    if st.checkbox("Show Raw Data"):
        st.write(df)

# Track Page (POST method equivalent in Streamlit)
def track(data):
    if data:
        os.makedirs("data", exist_ok=True)
        file_exists = os.path.isfile(TRACKING_FILE)
        with open(TRACKING_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['User ID', 'Session ID', 'Page', 'Page Title', 'Clicks', 'Avg Time Spent'])
            writer.writerow([
                data.get('user_id'),
                data.get('session_id'),
                data.get('page', '').lower().strip(),
                data.get('page_title'),
                data.get('clicks'),
                data.get('avg_time_spent')
            ])

# Simulate tracking (for testing)
def simulate_tracking():
    st.subheader("📥 Simulate Tracking Input")
    user_id = st.text_input("User ID")
    session_id = st.text_input("Session ID")
    page = st.text_input("Page")
    page_title = st.text_input("Page Title")
    clicks = st.number_input("Clicks", min_value=0, step=1)
    avg_time_spent = st.number_input("Average Time Spent (seconds)", min_value=0.0, step=0.1)

    if st.button("Submit Tracking Data"):
        data = {
            "user_id": user_id,
            "session_id": session_id,
            "page": page,
            "page_title": page_title,
            "clicks": clicks,
            "avg_time_spent": avg_time_spent
        }
        track(data)
        st.success("Tracking data submitted successfully!")

if __name__ == '__main__':
    main()
