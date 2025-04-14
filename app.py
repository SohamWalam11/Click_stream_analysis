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
from flask import Flask, request, jsonify, render_template
from pyngrok import ngrok  # ✅ Added for public URL
import csv
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__, static_folder="static", template_folder="templates")
TRACKING_FILE = os.path.join("data", "tracking.csv")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/dashboard')
def dashboard():
    if not os.path.isfile(TRACKING_FILE):
        return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

    df = pd.read_csv(TRACKING_FILE)

    if df.empty:
        return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

    # Normalize and check required columns
    df.columns = df.columns.str.strip()
    df['Page'] = df['Page'].str.lower().str.strip()

    required_columns = {'Page', 'Clicks', 'Avg Time Spent'}
    if not required_columns.issubset(df.columns):
        print("Missing required columns in tracking.csv:", df.columns.tolist())
        return render_template("dashboard.html", tracking=[], summary=[], bar_chart="", pie_chart="", time_chart="")

    # Grouping for summary
    summary = df.groupby('Page').agg({
        'Clicks': 'sum',
        'Avg Time Spent': 'mean'
    }).reset_index()

    # Visualizations
    bar_fig = px.bar(summary, x='Page', y='Clicks', title='📊 Clicks per Page', color='Page')
    bar_html = pio.to_html(bar_fig, full_html=False)

    pie_fig = px.pie(summary, names='Page', values='Clicks', title='📈 Click Distribution by Page')
    pie_html = pio.to_html(pie_fig, full_html=False)

    time_fig = px.bar(summary, x='Page', y='Avg Time Spent', title='⏱️ Average Time Spent per Page (s)', color='Page')
    time_html = pio.to_html(time_fig, full_html=False)

    return render_template(
        'dashboard.html',
        tracking=df.to_dict(orient='records'),
        summary=summary.to_dict(orient='records'),
        bar_chart=bar_html,
        pie_chart=pie_html,
        time_chart=time_html
    )

@app.route('/track', methods=['POST'])
def track():
    data = request.get_json()
    print(f"Received tracking data: {data}")

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
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # ✅ Create a public URL using ngrok
    public_url = ngrok.connect(5000)
    print(" * Public URL:", public_url)

    # Run Flask app
    app.run(port=5000, debug=True)
