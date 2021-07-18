import re
from datetime import datetime

from flask import request, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from jinja2 import evalcontextfilter, Markup
from werkzeug.security import generate_password_hash, check_password_hash

from simple_notes import app, db, login_manager
from simple_notes.models import Users, Notes


@app.template_filter()
@evalcontextfilter
def linebreaks(_eval_ctx, value):
    # https://gist.github.com/cemk/1324543
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


@app.template_filter()
@evalcontextfilter
def linebreaksbr(_eval_ctx, value):
    # https://gist.github.com/cemk/1324543
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'%s' % p.replace('\n', '<br/>') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


@login_manager.unauthorized_handler
def unauthorized_callback():
    # if unauthorized then redirect to login
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    # load user by id from database
    return Users.query.filter_by(id=user_id).first()


@app.route('/register', methods=("POST", "GET"))
def register():
    if current_user.is_authenticated:
        print(current_user)
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_2 = request.form['password_2']
        # ... check valid ...
        if password == password_2 and password != '' and email != '' and username != '':
            try:
                hash_pass = generate_password_hash(password)
                user = Users(email=email, username=username, password=hash_pass)
                db.session.add(user)
                db.session.flush()
                db.session.commit()
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                print(e)
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('notes'))
        else:
            print('pizda')
            pass
    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('notes'))


@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/secret', methods=['GET'])
@login_required
def secret():
    return render_template('secret.html')


@app.route('/', methods=['GET'])
@login_required
def notes():
    curr_user_id = Users.query.filter_by(id=current_user.id).first().id
    curr_user_notes = Notes.query.filter_by(user_id=curr_user_id).all()
    return render_template('notes.html', notes=curr_user_notes)


@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    title = request.form['title']
    details = request.form['details']
    curr_user_id = Users.query.filter_by(id=current_user.id).first().id
    if title != '':
        note = Notes(user_id=curr_user_id, title=title, detail_text=details)
        db.session.add(note)
        db.session.flush()
        db.session.commit()
    return redirect(url_for('notes'))


@app.route('/notes/<note_id>', methods=['GET'])
@login_required
def note_detail(note_id):
    curr_user_id = Users.query.filter_by(id=current_user.id).first().id
    note = Notes.query.filter_by(user_id=curr_user_id, id=note_id).first()
    return render_template('details.html', note=note)


@app.route('/delete_note/<note_id>', methods=['GET'])
@login_required
def delete_note(note_id):
    curr_user_id = Users.query.filter_by(id=current_user.id).first().id
    Notes.query.filter_by(user_id=curr_user_id, id=note_id).delete()
    db.session.flush()
    db.session.commit()
    return redirect(url_for('notes'))


@app.route('/edit_note/<note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    title = request.form['title']
    details = request.form['details']
    curr_user_id = Users.query.filter_by(id=current_user.id).first().id
    if title != '':
        Notes.query.filter_by(user_id=curr_user_id, id=note_id).update(
            {'title': title, 'detail_text': details, 'date_upd': datetime.utcnow()})
        db.session.flush()
        db.session.commit()
    return redirect(url_for('note_detail', note_id=note_id))

