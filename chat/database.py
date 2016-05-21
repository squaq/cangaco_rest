from chat import app, db
from chat.model.user import User

db_session = db.session


@app.teardown_request
def teardown_request(exception):
    """ Called after response has been constructed """
    db_session.remove()


def get_all_users():
    """
    Lists the keys and computer ids.
    :return:
    """
    all_keys = User.query.all()
    result = [l.get_dict() for l in all_keys]
    return result


def add_new_user(user_id, email, name):
    user = User(user_id=user_id, email=email, name=name)
    db_session.add(user)
    db_session.commit()
    return user.get_dict()


def get_user(user_id):
    result = User.query.filter_by(user_id=user_id).first()
    if result is None:
        return None
    return result.get_dict()


def get_all_users():
    return User.query.all()
