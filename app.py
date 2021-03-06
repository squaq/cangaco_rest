"""
Run the CHAT server
"""
from chat import app, socketio

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    socketio.run(app, policy_server=False, transports='websocket, xhr-polling, xhr-multipart')
