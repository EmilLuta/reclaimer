from app.models import User

from app import db

user = User(
    first_name='Test',
    last_name='Test',
    email='test@test.test',
    picture_url='x',
    social_id='x',
    social_profile_url='x',
)

db.session.add(user)
db.session.commit()
