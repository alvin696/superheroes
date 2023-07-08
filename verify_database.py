import os
from flask import Flask

app = Flask(__name__)

# Set the SQLALCHEMY_DATABASE_URI configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'

# Extract the file path from the configuration
database_uri = app.config['SQLALCHEMY_DATABASE_URI']
database_file_path = database_uri.replace('sqlite:///', '')

# Validate the file path
if os.path.exists(database_file_path):
    print("The database file exists.")
else:
    print("The database file does not exist or the path is incorrect.")
