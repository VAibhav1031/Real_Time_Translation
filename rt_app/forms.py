from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class JoinChatForm(FlaskForm):
    room = StringField("room", validators=[DataRequired()])
    role  = SelectField("role",choices=[("doctor","Doctor"),("patient","Patient")], validators=[DataRequired()])
    language = SelectField("language", choices=[("en","English"),("hi","Hindi"),("es","Spanish"),("fr","French")])
    submit = SubmitField("Join Chat")
