from chat import app, controller
from flask import jsonify, request, abort, render_template, session, redirect, url_for
from forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def index():
    """"Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@app.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)


# @app.route('/')
# def index_page():
#     return render_template('index.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    if not request.json:
        abort(400)
    if any(x not in request.json for x in {'user_id', 'email', 'name'}):
        abort(404, 'Missing parameters.')
    req_json = request.json
    app.logger.info(u'Adding new user: {}'.format(req_json))
    res = controller.register_new_user(req_json['user_id'], req_json['email'], req_json['name'])
    return jsonify({'new_user': res})


@app.route('/fetch_channels', methods=['get'])
def get_channels():
    if 'user_id' not in request.headers:
        abort(400, 'User not specified')
    user = request.headers['user_id']
    app.logger.info(u'Sending channels to: {}'.format(user))
    return jsonify({'channel_list': controller.get_channels()})


@app.route('/fetch_offline_messages', methods=['get'])
def get_offline_messages():
    if 'user_id' not in request.headers:
        abort(404, 'User not specified')
    user = request.headers['user_id']
    app.logger.info(u'Sending Offline messages to: {}'.format(user))
    return jsonify({'channel_list': controller.get_offline_messages()})


@app.route('/fetch_all_users', methods=['get'])
def get_all_users():
    if 'user_id' not in request.headers:
        abort(404, 'User not specified')
    user = request.headers['user_id']
    app.logger.info(u'User {} fetching list of users.'.format(user))
    return jsonify({'users_list': controller.get_all_users()})



