from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("login")

class SearchSetsBySets(FlaskForm):
    max_parts=IntegerField("Max parts", validators=[NumberRange(min=1)])
    submit= SubmitField("Search")

class SearchForm(FlaskForm):
    search_string=StringField("Search", validators=[DataRequired(), Length(min=4, message="Пожалуйста введите минимум 4 символа!")])
    submit= SubmitField("Search")