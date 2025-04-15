import streamlit as st
import pandas as pd
import plotly.express as px
import os
import csv
import time
from datetime import datetime

# Constants
TRACKING_FILE = os.path.join("data", "tracking.csv")
PAGES = ["Home", "About", "Products", "Dashboard"]

# Function to track clicks and time spent
def track_page_visit(current_page):
    now = time.time()
    if "last_visited_page" in st.session_state and "entry_time" in st.session_state:
        last_page = st.session_state["last_visited_page"]
        entry_time = st.session_state["entry_time"]
        time_spent = round(now - entry_time, 2)

        if last_page != "Dashboard":  # We don't track time on Dashboard
            save_tracking_data({
                "user_id": "guest",  # can be extended
                "session_id": st.session_state.get("session_id", "anonymous"),
                "page": last_page,
                "page_title": last_page,
                "clicks": 1,
                "avg_time_spent": time_spent
            })

    # Update session state for new page
    st.session_state["last_visited_page"] = current_page
    st.session_state["entry_time"] = now
    st.session_state["session_id"] = st.session_state.get("session_id", str(int(now)))  # dummy session_id

# Save to CSV
def save_tracking_data(data):
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

# Main Page
def main():
    st.title("Clickstream Tracking Dashboard")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", PAGES)

    track_page_visit(page)  # 👈 Track every time a new page is visited

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

# Dashboard Page
def dashboard():
    st.subheader("📊 Analytics Dashboard")

    if not os.path.isfile(TRACKING_FILE):
        st.warning("No data available.")
        return

    df = pd.read_csv(TRACKING_FILE)
    
    if df.empty:
        st.warning("No data available.")
        return

    df.columns = df.columns.str.strip()
    df['Page'] = df['Page'].str.lower().str.strip()

    required_columns = {'Page', 'Clicks', 'Avg Time Spent'}
    if not required_columns.issubset(df.columns):
        st.error("Missing required columns in tracking.csv")
        return

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

    if st.checkbox("Show Raw Data"):
        st.write(df)

if __name__ == '__main__':
    main()
