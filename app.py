from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import json
import os
import logging
import csv
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16)) 


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
        csv_file_path = os.path.join(app.root_path, 'dataStore.csv')

        try:
            # Append the data to the CSV file
            with open(csv_file_path, mode='a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                # Write header only if the file is new
                if csv_file.tell() == 0:
                    writer.writerow(['Name', 'Email', 'Phone', 'Message'])  # Write header
                writer.writerow([name, email, phone, message])
            flash('Contact saved successfully!')
            return redirect(url_for('contact_page'))
        except Exception as e:
            logging.error(f"Error saving contact: {e}")
            flash('Error saving contact. Please try again.', 'error')

    return render_template('contact.html')
@app.route('/projects')
def projects_page():
    return render_template('projects.html', title="Projects", cards=get_projects())

@app.route('/resume')
def resume():
    return send_file("static/assets/fucking_idiot.png", as_attachment=True)