from flask import Flask, request
import logging
import os  # Import os for environment variables
from app.routes import routes_bp  # Import blueprint for routes
from app.api import api_bp        # Import blueprint for API

# Initialize the app instance
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Register blueprints
app.register_blueprint(routes_bp)
app.register_blueprint(api_bp)

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)  # This is sufficient, no need to call it twice
app.logger.setLevel(logging.DEBUG)  # Set the Flask logger to DEBUG level for detailed logging

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

# Handle 500 Internal Server Errors
@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Server error: {error}")
    return "500 error", 500

# Add Content Security Policy header
@app.after_request
def set_csp_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.plot.ly 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "font-src 'self' data:; "
        "img-src 'self' data:; "
        "connect-src 'self' https://cdn.plot.ly;"  # Allow external data fetching
    )
    return response


# Run the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))  # Default to 8000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=port)
