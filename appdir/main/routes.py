from appdir import db, key
from flask import render_template, flash, redirect, url_for, request, send_from_directory, send_file
from flask_login import current_user, login_user, logout_user, login_required
from appdir.models import User, Message
from appdir.main.forms import ComposeForm, DbdumpForm
from werkzeug.urls import url_parse
from cryptography.fernet import Fernet
import gzip
import delegator
from appdir.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        messages = Message.query.filter_by(recipient_id = current_user.id).all()
        print(messages)
    return render_template('index.html', title='Index', messages = messages)

@bp.route('/message/<message_id>')
@login_required
def message(message_id):
    if current_user.is_authenticated:
        message = Message.query.filter_by(recipient_id = current_user.id, id = message_id ).first()
        if message:
            return render_template('message.html',title='Message', message=message)
    return redirect(url_for('main.index'))  

    
@bp.route('/compose',methods=['GET','POST'])
@login_required
def compose():
    if current_user.is_authenticated:
        form = ComposeForm()
        users = User.query.filter(User.id != current_user.id).all()
        users_list = [(i.id,i.username) for i in users]
        form.username.choices = users_list
        if form.validate_on_submit():
            f = Fernet(key)
            encrypted_message = f.encrypt(form.content.data.encode()).decode('utf-8')
            m = Message(content_crypt=encrypted_message, sender_id=current_user.id, recipient_id=form.username.data)
            db.session.add(m)
            db.session.commit()
            flash('Message created')
            return redirect(url_for('main.index'))
        return render_template('compose.html', title='Compose', form=form)

        
@bp.route('/dbdump', methods=['GET','POST'])
def dbdump():
    form =  DbdumpForm()
    if form.validate_on_submit():
        with gzip.open('appdir/backupII.gz', 'wb') as f:
            c = delegator.run('pg_dump -h localhost -p 5432 -U postgres messagum')
            f.write(c.out.encode('utf-8'))
        return send_file('appdir/backupII.gz', as_attachment=True)
    return render_template('dbdump.html', title='Dbdump', form=form)

