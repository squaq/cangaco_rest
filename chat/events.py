from flask.ext.socketio import emit, join_room, leave_room, send
from chat import socketio, app


@socketio.on('connect', namespace='/chat')
def connect_user():
    emit('success', 'Welcome to the Room')


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message.get('room')
    user = message.get('user')
    join_room(room)
    app.logger.info('User %s joined %s room' % (user, room))
    emit('status', {'msg': user + ' has entered the room.', 'username': user}, room=room)


@socketio.on('new message', namespace='/chat')
def send_message(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message.get('room')
    user = message.get('user')
    emit('new message', {'username': user, 'msg': message['msg']}, room=room)


# @socketio.on('typing', namespace='/chat')
# def typing_message(message):
#     """Sent by a client when the user entered a new message.
#     The message is sent to all people in the room."""
#     room = message.get('room')
#     user = message.get('user')
#
#     emit('typing', {'msg': user + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = message.get('room')
    user = message.get('user')
    leave_room(room)
    emit('user left', {'msg': user + ' has left the room.'}, room=room)


@socketio.on('leave', namespace='/chat')
def on_leave(data):
    room = data.get('room')
    user = data.get('user')
    leave_room(room)
    emit('status', {'msg': user + ' has left the room.'}, room=room)
    send(user + ' has left the room.', room=room)
