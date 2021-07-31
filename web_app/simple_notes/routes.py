from datetime import datetime

from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from simple_notes import app, db, login_manager
from simple_notes.models import Users, Notes


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
        return redirect(url_for('notes'))
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
                flash('User was created. Please sign in.', category='ok')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                print(e)
                flash('Error in the registration form', category='err')
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('notes'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = True if request.form.get("remember-me") else False

        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            return redirect(url_for('notes'))
        else:
            print('fail login')
            flash('Password and login do not match', category='err')
            pass
    return render_template('login.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('notes'))


@app.route('/', methods=['GET'])
@login_required
def notes():
    curr_user_notes = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.date_creat.desc()).all()
    return render_template('notes.html', notes=curr_user_notes)


@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    title = request.form['title']
    details = request.form['details']
    if title != '':
        note = Notes(user_id=current_user.id, title=title, detail_text=details)
        db.session.add(note)
        db.session.flush()
        db.session.commit()
    return redirect(url_for('notes'))


@app.route('/notes/<note_id>', methods=['GET'])
@login_required
def note_detail(note_id):
    note = Notes.query.filter_by(user_id=current_user.id, id=note_id).first()
    return render_template('details.html', note=note)


@app.route('/delete_note/<note_id>', methods=['GET'])
@login_required
def delete_note(note_id):
    Notes.query.filter_by(user_id=current_user.id, id=note_id).delete()
    db.session.flush()
    db.session.commit()
    return redirect(url_for('notes'))


@app.route('/edit_note/<note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    title = request.form['title']
    details = request.form['details']
    if title != '':
        Notes.query.filter_by(user_id=current_user.id, id=note_id).update(
            {'title': title, 'detail_text': details, 'date_upd': datetime.utcnow()})
        db.session.flush()
        db.session.commit()
    return redirect(url_for('note_detail', note_id=note_id))

