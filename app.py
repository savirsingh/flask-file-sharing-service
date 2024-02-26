# code by savir singh

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filesharing.db'  # Set the path to the SQLite database file
db = SQLAlchemy(app)  # Initialize the SQLAlchemy object for database operations
ADMIN_PASSWORD = 'YOUR_ADMIN_PASSWORD'  # Set the admin password
DIRECTORY = 'ROOT_DIRECTORY' # change this to the root directory for this project

# Define the File class to represent files in the database
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Define the route for the homepage
@app.route('/')
def index():
    # Check if the 'is_admin' cookie is set
    if request.cookies.get('is_admin'):
        # If the cookie is set, query all files from the database and render the index.html template
        files = File.query.all()
        return render_template('index.html', files=files)
    # If the cookie is not set, return a message
    return "Not validated yet."

# Define the route for the start page, which sets a cookie to validate the user as admin
@app.route('/start/<pw>')
def start(pw):
    # Check if the password provided matches the admin password
    if pw == ADMIN_PASSWORD:
        # If the password matches, create a response object with a redirect to the homepage and set the 'is_admin' cookie
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('is_admin', 'true')
        return resp
    # If the password does not match, return a message
    return "Password incorrect."

# Define the route for uploading files
@app.route('/upload', methods=['POST'])
def upload():
    # Check if the 'is_admin' cookie is set
    if request.cookies.get('is_admin'):
        # If the cookie is set, get the uploaded file and save it to the server
        file = request.files['file']
        filename = file.filename
        file.save(filename)

        # Get the password for the file from the form
        password = request.form.get('password')

        # Create a new File object with the filename, filepath, and password, and add it to the database
        new_file = File(filename=filename, filepath=filename, password=password)
        db.session.add(new_file)
        db.session.commit()

        # Redirect the user to the homepage
        return redirect(url_for('index'))
    # If the cookie is not set, return a message
    return "Not validated yet."

# Define the route for downloading files
@app.route('/download/<int:id>', methods=['GET', 'POST'])
def download(id):
    # Query the file with the specified id from the database
    file = File.query.get(id)
    if request.method == 'POST':
        # If the request method is POST, check if the password provided matches the file's password
        password = request.form.get('password')
        if password == file.password:
            # If the password matches, send the file as an attachment
            return send_from_directory(DIRECTORY,file.filepath, as_attachment=True)
        else:
            # If the password does not match, return a message
            return "Invalid password"
    # If the request method is not POST, render the download.html template with the file object
    return render_template('download.html', file=file)

# Run the Flask application
if __name__ == '__main__':
    # Create all database tables
    db.create_all()
    # Run the Flask application
    app.run()
