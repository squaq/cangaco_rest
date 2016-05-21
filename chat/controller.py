from chat import database


def get_channels():
    """Retrieves all channels registered"""
    return ['recife', 'brazil', 'boa vista']


def get_offline_messages(user_id):
    return 'none'


def get_all_users():
    list = database.get_all_users()

    return [l.get_dict() for l in list]


def get_user_info(user_id):
    return database.get_user(user_id=user_id)


def register_new_user(user_id, email, name):
    contains = database.get_user(user_id)
    if not contains:
        return database.add_new_user(user_id, email, name)
    return contains
