from rt_app import db
class Conversation(db.Model):

    __tablename__ = "conversation"

    id = db.Column(db.Integer, primary_key=True)
    room= db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    audio_message = db.Column(db.String,default=None)
    translated_text = db.Column(db.String, default=None)
    timestamp = db.Column(db.DateTime(timezone=True), default=None)


class RoomUser(db.Model):
    __tablename__ = "roomuser"

    id = db.Column(db.Integer, primary_key=True)
    room= db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    language = db.Column(db.String(20),nullable=False)
