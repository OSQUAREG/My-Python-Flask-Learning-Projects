from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    EmailField,
    PasswordField,
    BooleanField,
    SubmitField,
    FileField,
    ValidationError
)
from wtforms.validators import EqualTo, Length, InputRequired, Email
from wtforms.widgets import TextArea, FileInput
from flask_wtf.file import FileField

# from flask_ckeditor import CKEditor, CKEditorField
from models import app

# Create SignUpForm Class
class SignUpForm(FlaskForm):
    firstname = StringField(
        label="First Name", validators=[InputRequired(message="*Required")]
    )
    lastname = StringField(
        label="Last Name", validators=[InputRequired(message="*Required")]
    )
    username = StringField(
        label="Username",
        validators=[
            InputRequired(message="*Required"),
            Length(
                min=5, max=25, message="Password must be between 5 and 15 characters"
            ),
        ],
    )
    email = StringField(
        label="Email",
        validators=[
            InputRequired(message="*Required"),
            Length(
                5, 120, message="Password must be between 5 and 120 characters"
            ),
        ],
    )
    password = PasswordField(
        label="Password",
        validators=[
            InputRequired(message="*Required"),
            Length(min=8, message="Password must be more than 8 characters"),
        ],
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[
            InputRequired(message="*Required"),
            EqualTo("password", message="Passwords do not match!"),
        ],
    )
    about_author = TextAreaField(label="About Author")

    # profile_pic = FileField(label="Profile Pic")

    is_admin = BooleanField(label="Set as Admin")
    submit = SubmitField(label="Sign Up")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")



# Create Login Form Class
class LoginForm(FlaskForm):
    username_email = StringField(
        label="Username/Email",
        validators=[
            InputRequired(message="*Required"),
            Length(
                min=5, max=25, message="Password must be between 5 and 15 characters"
            ),
        ],
    )
    password = PasswordField(
        label="Password",
        validators=[
            InputRequired(message="*Required"),
            Length(min=8, message="Password must be more than 8 characters"),
        ],
    )
    submit = SubmitField(label="Login")


# test form
class TestForm(FlaskForm):
    comment = StringField(label="Name", validators=[InputRequired()], widget=TextArea())
    # email = StringField (label="Email", validators=[InputRequired()])
    submit = SubmitField(label="Submit")