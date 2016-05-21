from chat import db
from chat.model.user import User


db.create_all()

u = User('sample_id', 'sample@email.com', 'Sample Name')
db.session.add(u)
db.session.commit()
