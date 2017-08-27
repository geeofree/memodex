from server.webapp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<User username: %s, public_id: %s>" % (self.username, self.public_id)
