import os

from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from chat import settings

# Init the flask framework server.
app = Flask(__name__)
# Sets the settings
app.config.from_object(settings)

# Using local database or default heroku
if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'postgresql+psycopg2://postgres@/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.logger.info('Initing DB')
db = SQLAlchemy(app)
# socketio = SocketIO(app, host='127.0.0.1', port=5000, policy_server=False, transports='websocket, xhr-polling, xhr-multipart')
app.logger.info('Initing socket')
socketio = SocketIO(app)


# We need to import only after creating the app
import routes
import events
