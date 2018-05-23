from flask import current_app, render_template, redirect, url_for, request, flash
from app.main import bp
from app import db
from flask_login import current_user, login_required
from datetime import datetime
from app.models import User, Clue
from app.main.forms import EditProfileForm

@bp.route("/")
@bp.route("/index")
def index():
    return render_template(
        "main/index.html"
    )

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    
@bp.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username.lower()).first_or_404()
    page = request.args.get("page", 1, type=int)
    clues = user.clues.order_by(Clue.timestamp.desc()).paginate(
        page,
        current_app.config["POSTS_PER_PAGE"],
        False
    )
    next_url = url_for(
        "main.user",
        username=user.username,
        page=clues.next_num
    ) if clues.has_next else None
    prev_url = url_for(
        "main.user",
        username=user.username,
        page=clues.prev_num
    ) if clues.has_prev else None
    return render_template(
        "main/user.html",
        user=user,
        clues=clues.items,
        next_url=next_url,
        prev_url=prev_url
    )

@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data.lower()
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username.lower()
        form.about_me.data = current_user.about_me
    return render_template(
        "main/edit_profile.html",
        title="Edit profile",
        form=form
    )