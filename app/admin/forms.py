from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length


class GameForm(Form):
    name = StringField('Nombre', validators=[Length(0, 255)])
    desc = TextAreaField('Description')
    submit = SubmitField('Submit')
