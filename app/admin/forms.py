from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField
from wtforms.validators import Length


class GameForm(Form):
    name = StringField('Name', validators=[Length(0, 255)])
    desc = TextAreaField('Description')
    players = SelectMultipleField('Players', coerce=int)
    submit = SubmitField('Submit')
