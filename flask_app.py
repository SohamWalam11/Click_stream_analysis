import os
import time
import csv
import pandas as pd
import plotly.express as px
import streamlit as st

# ✅ Set page config as the first Streamlit command
st.set_page_config(
    page_title="Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# === Constants ===
TRACKING_FILE = os.path.join("data", "tracking.csv")
CLICK_LOG_FILE = os.path.join("data", "click_log.csv")
PAGES = ["Home", "About", "Products", "Dashboard"]

# === Save visit info ===
def save_tracking_data(data):
    os.makedirs("data", exist_ok=True)

    for file in [TRACKING_FILE, CLICK_LOG_FILE]:
        file_exists = os.path.isfile(file)
        with open(file, 'a', newline='') as f:
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

# === Track user on each page ===
def track_page_visit(current_page):
    now = time.time()
    last_page = st.session_state.get("last_visited_page")
    entry_time = st.session_state.get("entry_time")

    if last_page and entry_time:
        time_spent = round(now - entry_time, 2)
        if last_page != "Dashboard":
            save_tracking_data({
                "user_id": "guest",
                "session_id": st.session_state.get("session_id", "anonymous"),
                "page": last_page,
                "page_title": last_page,
                "clicks": 1,
                "avg_time_spent": time_spent
            })

    st.session_state["last_visited_page"] = current_page
    st.session_state["entry_time"] = now
    st.session_state["session_id"] = st.session_state.get("session_id", str(int(now)))

# === Home Page ===
def home():
    track_page_visit("Home")
    st.title("🏠 Home Page")
    st.write("Welcome to the Home Page")

# === About Page ===
def about():
    track_page_visit("About")
    st.title("ℹ️ About Page")
    st.write("This is the About Page")

# === Products Page ===
def products():
    track_page_visit("Products")
    st.title("🛍️ Products Page")
    st.write("Explore our Products")

# === Dashboard Page ===
def dashboard():
    track_page_visit("Dashboard")
    st.title("📊 Analytics Dashboard")

    summary = []
    raw_data = None

    if os.path.isfile(TRACKING_FILE):
        df = pd.read_csv(TRACKING_FILE)
        if not df.empty:
            df.columns = df.columns.str.strip()
            df['Page'] = df['Page'].str.lower().str.strip()

            summary_df = df.groupby('Page').agg({
                'Clicks': 'sum',
                'Avg Time Spent': 'mean'
            }).reset_index()

            # Charts
            bar_fig = px.bar(summary_df, x='Page', y='Clicks', title='Clicks per Page', color='Page')
            pie_fig = px.pie(summary_df, names='Page', values='Clicks', title='Click Distribution by Page')
            time_fig = px.bar(summary_df, x='Page', y='Avg Time Spent', title='Avg Time Spent per Page', color='Page')

            # Summary Table
            st.subheader("📌 Summary Table")
            st.dataframe(summary_df)

            # Display Charts
            st.subheader("📈 Clicks per Page")
            st.plotly_chart(bar_fig, use_container_width=True)

            st.subheader("📊 Click Distribution")
            st.plotly_chart(pie_fig, use_container_width=True)

            st.subheader("⏱️ Avg Time Spent per Page")
            st.plotly_chart(time_fig, use_container_width=True)

    # Show Raw Data
    if st.button("Show Raw Click Data") and os.path.exists(CLICK_LOG_FILE):
        raw_df = pd.read_csv(CLICK_LOG_FILE)
        st.subheader("🧾 Raw Data")
        st.dataframe(raw_df)

# === Main Function ===
def main():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(int(time.time()))

    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio("Go to", PAGES)

    if page == "Home":
        home()
    elif page == "About":
        about()
    elif page == "Products":
        products()
    elif page == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()
