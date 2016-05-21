import os
from chat import settings
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(settings)

if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'postgresql+psycopg2://postgres@/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)


# We need to import the controller so it can be init
import view