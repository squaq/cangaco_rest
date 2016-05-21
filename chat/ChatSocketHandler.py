import gevent
from flask_socketio import SocketIO, emit
from chat import app
import logging


class ChatBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self, redis_server, channel):
        socketio = SocketIO(app)
        self.clients = list()
        self.pubsub = redis_server.pubsub()
        self.pubsub.subscribe(channel)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'Sending message: {}'.format(data))
                yield data

    def register(self, client):
        """Register a WebSocket connection for Redis updates."""
        self.clients.append(client)

    def send(self, client, data):
        """Send given data to the registered client.
        Automatically discards invalid connections."""
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """Listens for new messages in Redis, and sends them to clients."""
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintains Redis subscription in the background."""
        gevent.spawn(self.run)


# @socketio.on('my event', namespace='/test')
# def test_message(message):
#     emit('my response', {'data': message['data']})
#
# @socketio.on('my broadcast event', namespace='/test')
# def test_message(message):
#     emit('my response', {'data': message['data']}, broadcast=True)
#
# @socketio.on('connect', namespace='/test')
# def test_connect():
#     emit('my response', {'data': 'Connected'})
#
# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected')


#
# @sockets.route('/submit')
# def inbox(ws):
#     """ Receives chat messages from WebScoket and adds into Redis"""
#     gevent.sleep(0.1)
#     message = ws.receive()
#     print message
#
#     if message:
#         app.logger.info(u'Inserting message: {}'.format(message))
#         redis_server.publish(REDIS_CHAN, message)
#
#
# @sockets.route('/receive')
# def outbox(ws):
#     """Sends outgoing chat messages, via `ChatBackend`."""
#     chats.register(ws)
#
#     while not ws.closed:
#         # Context switch while `ChatBackend.start` is running in the background.
#         gevent.sleep(0.1