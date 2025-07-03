from utilities import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)