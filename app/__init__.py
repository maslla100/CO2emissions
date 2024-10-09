
from flask import Flask, render_template

# Initialize the Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
