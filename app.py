from flask import Flask, render_template,send_file
import json
import os
import logging

app = Flask(__name__)




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
    return render_template('error.html', message='404 Page Not Found'), 404


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
    return render_template('contact.html', title='Contact Page')


@app.route('/projects')
def projects_page():
    return render_template('projects.html', title="Projects", cards=get_projects())

@app.route('/resume')
def resume():
    return send_file("static/assets/fucking_idiot.png", as_attachment=True)