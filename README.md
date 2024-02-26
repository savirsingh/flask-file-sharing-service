# Flask File Sharing Service

This is a simple file sharing web application built using Flask and SQLAlchemy. Users can upload files, which are stored on the server, and then download them using a password.

## Features

- Upload files with a password
- Download files using the password
- Admin access to manage files

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/file-sharing-app.git
   ```
2. Install the dependencies:
   ```bash
   pip install Flask Flask-SQLAlchemy
   ```
3. Set up the database:
   - Ensure you have SQLite installed.
   - Run the following commands in the project directory:
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```
4. Set the admin password:
   - Open `app.py` and set the `ADMIN_PASSWORD` variable to your desired admin password.
5. Run the application
   ```bash
   python app.py
   ```
6. Access the application in your browser at http://localhost:5000.

## Usage

- Visit the homepage (`/`) to see uploaded files.
- To upload a file, go to `/start/<admin_password>`and enter the admin password.
- Once validated, go to `/upload` to upload a file with a password.
- To download a file, go to `/download/<file_id>` and enter the file's password. Of course, non-admins can download files.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
