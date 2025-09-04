from CTFd.models import db
import datetime


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, challenge_id, user_id, rating, comment=None):
        self.challenge_id = challenge_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
