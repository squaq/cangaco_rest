from chat import app, db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, user_id, email, name):
        self.user_id = user_id
        self.email = email
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.user_id

    def get_dict(self):
        return dict(id=self.id, user_id=self.user_id, email=self.email,
                    name=self.name)
