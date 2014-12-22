from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField, BooleanField
from wtforms.validators import Length, Required


class GameForm(Form):
    name = StringField('Name', validators=[Required(), Length(0, 255)])
    desc = TextAreaField('Description')
    players = SelectMultipleField('Players', validators=[Required()], coerce=int)
    submit = SubmitField('Submit')


class EndGameForm(Form):
    endme = BooleanField('End this game?')
    submit = SubmitField('End Game')
