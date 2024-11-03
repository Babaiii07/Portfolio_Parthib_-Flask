from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import json
import os
import logging
import csv
import secrets
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16)) 


EDGE_CONFIG_API_URL = "https://edge-config.vercel.com/ecfg_pe7qtpumk2rrpz1ztcvvi8s7gfr0?token=c6499ee0-1599-4dd9-adcb-f07f5887e931"
EDGE_CONFIG_TOKEN = ""

headers = {
    'Authorization': f'Bearer {EDGE_CONFIG_TOKEN}',
    'Content-Type': 'application/json'
}

def get_projects():
    try:
        file_path = os.path.join(app.root_path, 'static', 'assets', 'projects.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                projects = json.load(file)
                return projects.get('projects', [])
        else:
            logging.error(f"File not found: {file_path}")
            return []
    except Exception as e:
        logging.error(f"Error loading projects.json: {e}")
        return []

@app.errorhandler(Exception)
def handle_exception(message):
    return render_template('error.html', message="Bad Request"), 400

@app.errorhandler(404)
def err_404(message):
    return render_template('404.html', message='404 Page Not Found'), 404

@app.route('/')
def main_page():
    return render_template('index.html', title='Parthib Karak - Homepage')

@app.route('/home')
def home():
    return render_template('base.html', title='Base')

@app.route('/about')
def about_page():
    return render_template('about.html', title="About")

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        # Data to store in Edge Config
        contact_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "message": message
        }

        try:
            response = requests.post(
                f"{EDGE_CONFIG_API_URL}/set-contact",  # Update with actual endpoint
                headers=headers,
                json=contact_data
            )
            response.raise_for_status()
            return "Contact saved successfully!"
        except requests.exceptions.RequestException as e:
            print(f"Error saving contact: {e}")
            return "Error saving contact.", 500

    return render_template('contact.html')

@app.route('/projects')
def projects_page():
    return render_template('projects.html', title="Projects", cards=get_projects())

@app.route('/resume')
def resume():
    return send_file("static/assets/fucking_idiot.png", as_attachment=True)