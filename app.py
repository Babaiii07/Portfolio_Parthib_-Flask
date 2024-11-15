from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import json
import os
import logging
import secrets
import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))


cred_path = os.path.join(os.path.dirname(__file__), 'static', 'assets', 'portfolio.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)


db = firestore.client()


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

@app.route('/projects')
def projects_page():
    return render_template('projects.html', title="Projects", cards=get_projects())

@app.route('/skills')
def skills_page():
    return render_template('skill.html', title="Skills")

@app.route('/resume')
def resume():
    return send_file("static/assets/fucking_idiot.png", as_attachment=True)

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        logging.info(f"Received contact form data: Name={name}, Email={email}, Phone={phone}, Message={message}")

  
        contacts_ref = db.collection('contacts')

        try:
    
            contacts_ref.add({
                'name': name,
                'email': email,
                'phone': phone,
                'message': message
            })
            flash('Contact saved successfully!', 'success')
            return redirect(url_for('contact_page'))
        except Exception as e:
            logging.error(f"Error saving contact to Firebase: {e}")
            flash('Error saving contact. Please try again.', 'error')
            return render_template('contact.html')  

    return render_template('contact.html')
