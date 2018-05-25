from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Username already in use")

class EditProfileFormAdmin(FlaskForm):
    user_id = StringField("User ID", validators=[DataRequired()])
    user_email = StringField("User Email")
    username = StringField("Username")
    about_me = TextAreaField("About me")
    submit = SubmitField("Submit")
    
    def validate_username(self, username): #checks if the username is in use
        if self.username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Username aldready in use")
    
    def validate_user_id(self, user_id): #Checks if the uid exists
        user = User.query.filter_by(id=self.user_id.data).first()
        if user is None:
            raise ValidationError("User_ID does not exist.")
    
    def validate_user_email(self, user_email): #Checks if the email is in use
        if self.user_email:
            user = User.query.filter_by(email=user_email.data).first()
            if user is not None:
                raise ValidationError("Email already in use!")