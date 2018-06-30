from flask import current_app, render_template, redirect, url_for, request, flash
from app.main import bp
from app import db
from flask_login import current_user, login_required
from datetime import datetime
from app.models import User, Clue, Rs_items
from app.main.forms import EditProfileForm, EditProfileFormAdmin
import json

@bp.route("/")
@bp.route("/index")
def index():
    site_admins = current_app.config["SITE_ADMINS"]
    return render_template(
        "main/index.html",
        site_admins=site_admins
    )

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route("/user/<username>")
def user(username):
    site_admins = current_app.config["SITE_ADMINS"]
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
        site_admins=site_admins,
        user=user,
        clues=clues.items,
        next_url=next_url,
        prev_url=prev_url
    )

@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    site_admins = current_app.config["SITE_ADMINS"]
    if current_user.id in site_admins:
        form = EditProfileFormAdmin()
        if form.validate_on_submit():
            user_id = form.user_id.data
            user = User.query.filter_by(id=user_id).first()

            if form.user_email.data:
                user.email = form.user_email.data
            if form.username.data:
                user.username = form.username.data.lower()
            if form.about_me.data:
                user.about_me = form.about_me.data
            db.session.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("main.edit_profile"))
    else:
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

@bp.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash ("User {} not found.").format(username)
        return redirect(url_for("main.index"))
    if user == current_user:
        flash("You can't follow yourself!")
        return redirect(url_for("main.user", username=username))
    current_user.follow(user)
    db.session.commit()
    flash("You are now following {}!".format(username))
    return redirect(url_for("main.user", username=username))

@bp.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User {} not found.".format(username))
        return redirect(url_for("main.index"))
    if user == current_user:
        flash("You can't unfollow yourself")
        return redirect(url_for("main.user", username=username))

    current_user.unfollow(user)
    db.session.commit()
    flash("You are not following {} anymore.".format(username))
    return redirect(url_for("main.user", username=username))

@bp.route("/add_rs_items")
def add_rs_items():
    json_data = open('objects_87.json').read()
    data = json.loads(json_data)

    for i in data:
        item = Rs_items(id=i["id"], name=i["name"].lower())
        db.session.add(item)
    db.session.commit()
    return redirect(url_for("index"))

@bp.route("/item/<rs_item>")
def item(rs_item):
    item = Rs_items.query.filter_by(name=rs_item).first()
    return render_template(
        "main/item.html",
        title=item.name
    )
