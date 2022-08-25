from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired
from datetime import datetime

class LoginForm(FlaskForm):
    uname = StringField("שם משתמש", validators=[DataRequired()])
    password = PasswordField("סיסמה", validators=[DataRequired()])
    submit = SubmitField("כניסה")