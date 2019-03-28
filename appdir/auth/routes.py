from appdir import db, key
from flask import render_template, flash, redirect, url_for, request, send_from_directory, send_file
from flask_login import current_user, login_user, logout_user, login_required
from appdir.models import User
from appdir.auth.forms import LoginForm, RegisterForm
from werkzeug.urls import url_parse
from appdir.auth import bp


@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data.lower(), email = form.email.data, first_name = form.first_name.data, last_name=form.last_name.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('User created')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
