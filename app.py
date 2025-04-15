# from flask import Flask, request, jsonify, render_template
# import csv
# import os
# import pandas as pd
# import plotly.express as px
# import plotly.io as pio

# app = Flask(__name__, static_folder="static", template_folder="templates")
# TRACKING_FILE = os.path.join("data", "tracking.csv")

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/products')
# def products():
#     return render_template('products.html')

# @app.route('/dashboard')
# def dashboard():
#     if not os.path.isfile(TRACKING_FILE):
#         return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

#     df = pd.read_csv(TRACKING_FILE)

#     if df.empty:
#         return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

#     # Normalize and check required columns
#     df.columns = df.columns.str.strip()
#     df['Page'] = df['Page'].str.lower().str.strip()

#     required_columns = {'Page', 'Clicks', 'Avg Time Spent'}
#     if not required_columns.issubset(df.columns):
#         print("Missing required columns in tracking.csv:", df.columns.tolist())
#         return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

#     # Grouping for summary
#     summary = df.groupby('Page').agg({
#         'Clicks': 'sum',
#         'Avg Time Spent': 'mean'
#     }).reset_index()

#     # Visualizations
#     bar_fig = px.bar(summary, x='Page', y='Clicks', title='📊 Clicks per Page', color='Page')
#     bar_html = pio.to_html(bar_fig, full_html=False)

#     pie_fig = px.pie(summary, names='Page', values='Clicks', title='📈 Click Distribution by Page')
#     pie_html = pio.to_html(pie_fig, full_html=False)

#     time_fig = px.bar(summary, x='Page', y='Avg Time Spent', title='⏱️ Average Time Spent per Page (s)', color='Page')
#     time_html = pio.to_html(time_fig, full_html=False)

#     return render_template(
#         'dashboard.html',
#         tracking=df.to_dict(orient='records'),
#         summary=summary.to_dict(orient='records'),
#         bar_chart=bar_html,
#         pie_chart=pie_html,
#         time_chart=time_html
#     )

# @app.route('/track', methods=['POST'])
# def track():
#     data = request.get_json()
#     print(f"Received tracking data: {data}")

#     if data:
#         os.makedirs("data", exist_ok=True)
#         file_exists = os.path.isfile(TRACKING_FILE)
#         with open(TRACKING_FILE, 'a', newline='') as f:
#             writer = csv.writer(f)
#             if not file_exists:
#                 writer.writerow(['User ID', 'Session ID', 'Page', 'Page Title', 'Clicks', 'Avg Time Spent'])
#             writer.writerow([
#                 data.get('user_id'),
#                 data.get('session_id'),
#                 data.get('page', '').lower().strip(),
#                 data.get('page_title'),
#                 data.get('clicks'),
#                 data.get('avg_time_spent')
#             ])
#     return jsonify({"status": "success"}), 200

# if __name__ == '__main__':
#     app.run(debug=True)
# from flask import Flask, request, jsonify, render_template
# from pyngrok import ngrok  # ✅ Added for public URL
# import csv
# import os
# import pandas as pd
# import plotly.express as px
# import plotly.io as pio

# app = Flask(__name__, static_folder="static", template_folder="templates")
# TRACKING_FILE = os.path.join("data", "tracking.csv")

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/products')
# def products():
#     return render_template('products.html')

# @app.route('/dashboard')
# def dashboard():
#     if not os.path.isfile(TRACKING_FILE):
#         return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

#     df = pd.read_csv(TRACKING_FILE)

#     if df.empty:
#         return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

#     # Normalize and check required columns
#     df.columns = df.columns.str.strip()
#     df['Page'] = df['Page'].str.lower().str.strip()

#     required_columns = {'Page', 'Clicks', 'Avg Time Spent'}
#     if not required_columns.issubset(df.columns):
#         print("Missing required columns in tracking.csv:", df.columns.tolist())
#         return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

#     # Grouping for summary
#     summary = df.groupby('Page').agg({
#         'Clicks': 'sum',
#         'Avg Time Spent': 'mean'
#     }).reset_index()

#     # Visualizations
#     bar_fig = px.bar(summary, x='Page', y='Clicks', title='📊 Clicks per Page', color='Page')
#     bar_html = pio.to_html(bar_fig, full_html=False)

#     pie_fig = px.pie(summary, names='Page', values='Clicks', title='📈 Click Distribution by Page')
#     pie_html = pio.to_html(pie_fig, full_html=False)

#     time_fig = px.bar(summary, x='Page', y='Avg Time Spent', title='⏱️ Average Time Spent per Page (s)', color='Page')
#     time_html = pio.to_html(time_fig, full_html=False)

#     return render_template(
#         'dashboard.html',
#         tracking=df.to_dict(orient='records'),
#         summary=summary.to_dict(orient='records'),
#         bar_chart=bar_html,
#         pie_chart=pie_html,
#         time_chart=time_html
#     )

# @app.route('/track', methods=['POST'])
# def track():
#     data = request.get_json()
#     print(f"Received tracking data: {data}")

#     if data:
#         os.makedirs("data", exist_ok=True)
#         file_exists = os.path.isfile(TRACKING_FILE)
#         with open(TRACKING_FILE, 'a', newline='') as f:
#             writer = csv.writer(f)
#             if not file_exists:
#                 writer.writerow(['User ID', 'Session ID', 'Page', 'Page Title', 'Clicks', 'Avg Time Spent'])
#             writer.writerow([
#                 data.get('user_id'),
#                 data.get('session_id'),
#                 data.get('page', '').lower().strip(),
#                 data.get('page_title'),
#                 data.get('clicks'),
#                 data.get('avg_time_spent')
#             ])
#     return jsonify({"status": "success"}), 200

# if __name__ == '__main__':
#     # ✅ Create a public URL using ngrok
#     public_url = ngrok.connect(5000)
#     print(" * Public URL:", public_url)

#     # Run Flask app
#     app.run(port=5000, debug=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os
import csv
from pyngrok import ngrok  # Used to expose the app to the public

# Constants
TRACKING_FILE = os.path.join("data", "tracking.csv")

# Create a public URL using ngrok (for testing purposes)
public_url = ngrok.connect(8501)
st.write("Public URL:", public_url)

# Main Page
def main():
    st.title("Clickstream Tracking Dashboard")

    # Home page
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Home", "About", "Products", "Dashboard"))

    if page == "Home":
        st.header("Welcome to the Clickstream Tracking System")
        st.write("This app tracks user activity across different pages.")
    elif page == "About":
        st.header("About")
        st.write("This is an app that tracks user behavior on various pages and provides insights like total clicks, average time spent per page, etc.")
    elif page == "Products":
        st.header("Products")
        st.write("Here you can view products and their details.")
    elif page == "Dashboard":
        dashboard()

# Dashboard Page
def dashboard():
    if not os.path.isfile(TRACKING_FILE):
        st.write("No data available.")
        return

    df = pd.read_csv(TRACKING_FILE)
    
    if df.empty:
        st.write("No data available.")
        return

    # Normalize and check required columns
    df.columns = df.columns.str.strip()
    df['Page'] = df['Page'].str.lower().str.strip()

    required_columns = {'Page', 'Clicks', 'Avg Time Spent'}
    if not required_columns.issubset(df.columns):
        st.write("Missing required columns in tracking.csv")
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
    # Run the Streamlit app
    main()
