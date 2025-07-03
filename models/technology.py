from utilities import db

class Technology(db.Model):
    __tablename__ = 'technologies'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, nullable=False)
    group = db.Column(db.Text, nullable=False)