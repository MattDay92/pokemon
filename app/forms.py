from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class PokemonSearchForm(FlaskForm):
    choose = StringField('Poke', validators = [DataRequired()])
    submit = SubmitField()
    catch_pokemon = SubmitField()


class CatchPokemon(FlaskForm):
    choose = StringField('Poke', validators = [DataRequired()])
    catch_pokemon = SubmitField()

class UserCreationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField()


    