from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, IssueForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Issues


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', version='0.01', issues=issues)

@app.route('/issues')
@login_required
def issues():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nieprawidłowe hasło lub nazwa użytkownika')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Logowanie', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/new_issue', methods = ['GET', 'POST'])
def new_issue():
    machines_list = ['','JANOME MB-4', 'JANOME MB-7', 'JUNO E1015']
    form = IssueForm()
    #form.machines_list.choices =
    form.owner.data = current_user.username
    if form.validate_on_submit():
        issue =Issues(
            owner=current_user.username,
            machines_model=request.form.get('machine'),
            serial_number=form.serial_number.data,
            part_number=form.part_number.data,
            quantity=1,
            part_name=form.part_name.data,
            where_is_part='Czeka na dostarczenie',
            exchange_status='Czeka na wydanie',
            janome_status='Niezgłoszone')
        db.session.add(issue)
        db.session.commit()
        flash("Dodano zgłoszenie serwisowe o nr: {}".format(issue.id))
    return render_template('/new_issue.html', title='Nowe zgłoszenie', form=form, machines_list=machines_list)

