from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

@bp.route("/login", methods=["GET", "POST"]) #HTML methods
def login():
    if current_user.is_authenticated: #Checks if there is a user logged in
        return redirect(url_for("main.index"))
    
    form = LoginForm() #The form from app.auth.forms

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first() #Check the database
        if user is None or not user.check_password(form.password.data): #Compares the input with the database
            flash("Invalid username or password.")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data) #The user gets logged in
        #Redirect to "next" page
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    
    return render_template(
        "auth/login.html",
        title="Sign in",
        form=form)

@bp.route("/logout")
def logout():
    logout_user() #The user gets logged out
    return redirect(url_for("main.index")) #Redirects to index

@bp.route("/register", methods=["GET", "POST"]) #Checks if the user is logged in
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    
    form = RegistrationForm() #The registration form from auth/forms.py

    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data) #Sets the username and email
        user.set_password(form.password.data) #Sets the password
        db.session.add(user)
        db.session.commit() #Commit to database
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login")) #Registered user directed to login
    
    return render_template(
        "auth/register.html",
        title="Register",
        form=form
    )

@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    pass