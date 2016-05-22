from chat import app, socketio

if __name__ == '__main__':
    socketio.run(app, policy_server=False, transports='websocket, xhr-polling, xhr-multipart')
