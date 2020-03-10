from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app.db import User
from app.oauth import VkSignIn


def index():
    return render_template('index.html')


def logout():
    logout_user()
    return redirect(url_for('index'))


def oauth_authorize():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = VkSignIn()
    return oauth.authorize()


def oauth_callback():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = VkSignIn()
    social_id, email, image_url, friends_count = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.objects(social_id=social_id).first()
    if not user:
        user = User(
            social_id=social_id,
            email=email,
            image_url=image_url,
            friends_count=friends_count,
        ).save()
    login_user(user, True)
    return redirect(url_for('index'))


def add_resources(app):
    app.add_url_rule('/', 'index', view_func=index)
    app.add_url_rule('/logout', 'logout', view_func=logout)
    app.add_url_rule('/authorize', 'authorize', view_func=oauth_authorize)
    app.add_url_rule('/callback', 'callback', view_func=oauth_callback)
