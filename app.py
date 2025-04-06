from flask import Flask, request, jsonify, send_from_directory, render_template
import csv
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')

@app.route('/about.html')
def about():
    return send_from_directory('templates', 'about.html')

@app.route('/products.html')
def products():
    return send_from_directory('templates', 'products.html')

@app.route('/dashboard.html')
def dashboard():
    if os.path.isfile('tracking.csv'):
        df = pd.read_csv('tracking.csv')

        # Prepare summary data
        summary = df.groupby('Page').agg({
            'Clicks': 'sum',
            'Avg Time Spent': 'mean'
        }).reset_index()

        # Prepare plots
        bar_fig = px.bar(summary, x='Page', y='Clicks', title='Clicks per Page', color='Page')
        bar_html = pio.to_html(bar_fig, full_html=False)

        pie_fig = px.pie(summary, names='Page', values='Clicks', title='Click Distribution by Page')
        pie_html = pio.to_html(pie_fig, full_html=False)

        time_fig = px.bar(summary, x='Page', y='Avg Time Spent', title='Average Time Spent per Page (s)', color='Page')
        time_html = pio.to_html(time_fig, full_html=False)

        return render_template('dashboard.html', tracking=df.to_dict(orient='records'),
                               summary=summary.to_dict(orient='records'),
                               bar_chart=bar_html, pie_chart=pie_html, time_chart=time_html)
    else:
        return "No tracking data found. Please generate some tracking data first."

@app.route('/track', methods=['POST'])
def track():
    data = request.get_json()
    print(f"Received tracking data: {data}")

    if data:
        file_exists = os.path.isfile('tracking.csv')
        with open('tracking.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['User ID', 'Session ID', 'Page', 'Page Title', 'Clicks', 'Avg Time Spent'])
            writer.writerow([
                data.get('user_id'),
                data.get('session_id'),
                data.get('page'),
                data.get('page_title'),
                data.get('clicks'),
                data.get('avg_time_spent')
            ])
    return jsonify({"status": "success"}), 200

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    app.run(debug=True)