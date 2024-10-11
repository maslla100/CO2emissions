from flask import Flask, render_template, request
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

# Define the static folder explicitly
app = Flask(__name__, template_folder='templates', static_folder='static')

# Log when the Flask app starts
@app.before_first_request
def before_first_request():
    logging.info("Flask application has started")

# Log every request
@app.before_request
def log_request_info():
    logging.info(f"Request Method: {request.method}, Request Path: {request.path}")
    logging.info(f"Request Headers: {request.headers}")
    if request.method in ['POST', 'PUT', 'PATCH']:
        logging.info(f"Request Body: {request.get_data()}")

@app.route('/')
def index():
    logging.info("Rendering the index.html page")
    return render_template('index.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))  # Default to 8080 if PORT is not set
    app.run(host='0.0.0.0', port=port)

