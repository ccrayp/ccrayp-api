from utilities import db

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    stack = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)