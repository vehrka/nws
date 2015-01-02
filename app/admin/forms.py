from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, SelectField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import Length, Required


class AddClassForm(Form):
    types = SelectField('Type', validators=[Required()], coerce=int)
    sides =  SelectField('Original Side', validators=[Required()], coerce=int)
    name = StringField('Name', validators=[Required(), Length(0, 150)])
    acro = StringField('Acronim', validators=[Required(), Length(0, 50)])
    submit = SubmitField('Submit')


class AddShipForm(Form):
    shpclass = SelectField('Class', validators=[Required()], coerce=int)
    name = StringField('Name', validators=[Required(), Length(0,100)])
    bearing = IntegerField('Bearing')
    speed = IntegerField('Speed')
    height = IntegerField('Height')
    lat = IntegerField('Latitude')
    lon = IntegerField('Longitude')


class AssignSideForm(Form):
    sides = SelectField('Side', validators=[Required()], coerce=int)
    submit = SubmitField('Submit')


class GameForm(Form):
    name = StringField('Name', validators=[Required(), Length(0, 255)])
    desc = TextAreaField('Description')
    players = SelectMultipleField('Players', validators=[Required()], coerce=int)
    submit = SubmitField('Submit')


class EndGameForm(Form):
    endme = BooleanField('End this game?')
    submit = SubmitField('End Game')
