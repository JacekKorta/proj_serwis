from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, IssueForm, EditIssueForm, UserForm, NewMachineForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Issues, Machines


@app.route('/')
@app.route('/index/', methods=['GET','POST'])
@login_required
def index():
#strona główna z niezakończonymi zgłoszeniami, dla danego użytkownika [PL]
    if current_user.user_type in ('admin', 'warehouse'):
        issues = Issues.query.filter(~Issues.janome_status.in_(['wymienione', 'odrzucone']))
    elif current_user.user_type in ('service'):
        issues = Issues.query.filter(Issues.owner == current_user.username,  ~Issues.janome_status.in_(['wymienione', 'odrzucone']))
    if 'edit' in request.form:
        issue = request.form.to_dict()
        issue_id = issue['form_id']
        return redirect(url_for('edit_issue', issue_id=issue_id))
    return render_template('index.html', issues=issues, title='Strona główna', version='0.01')

@app.route('/issues/', methods=['GET','POST'])
@login_required
def issues():
#is showing the list of issues
    if current_user.user_type in ('admin', 'warehouse'):
        issues = Issues.query.order_by(Issues.id).all()
    elif current_user.user_type in ('service'):
        issues = Issues.query.filter(Issues.owner == current_user.username).order_by(Issues.id).all()
    if 'edit' in request.form:
        issue = request.form.to_dict()
        issue_id = issue['form_id']
        return redirect(url_for('edit_issue', issue_id=issue_id))

    return render_template('issues.html', issues=issues)

@app.route('/login/', methods=['GET', 'POST'])
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

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/new_issue/', methods = ['GET', 'POST'])
@login_required
def new_issue():
    machines_list = Machines.query.order_by(Machines.name).all()
    form = IssueForm()
    form.owner.data = current_user.username
    if form.validate_on_submit():
        issue =Issues(
            owner=current_user.username,
            machine_model=request.form.get('machine'),
            serial_number=form.serial_number.data,
            part_number=form.part_number.data,
            quantity=1,
            part_name=form.part_name.data,
            issue_desc = form.issue_desc.data,
            where_is_part='nowe',
            exchange_status='nowe',
            janome_status='niezgłoszone')
        db.session.add(issue)
        db.session.commit()
        flash("Dodano zgłoszenie serwisowe o nr: {}".format(issue.id))
        return redirect(url_for('issues'))
    return render_template('/new_issue.html', title='Nowe zgłoszenie', form=form, machines_list=machines_list)

@app.route('/edit_issue/<issue_id>', methods=['GET', 'POST'])
@login_required

def edit_issue(issue_id):
    current_issue = Issues.query.filter_by(id=issue_id).first()
    machines_list = Machines.query.order_by(Machines.name).all()
    form = EditIssueForm()
    if current_user.username == current_issue.owner:
        if form.validate_on_submit():
            current_issue.owner = form.owner.data
            current_issue.machine_model = form.machine_name.data
            current_issue.serial_number = form.serial_number.data
            current_issue.part_number = form.part_number.data
            current_issue.quantity = form.quantity.data
            current_issue.part_name = form.part_name.data
            current_issue.issue_desc = form.issue_desc.data
            current_issue.where_is_part = form.where_is_part.data
            current_issue.exchange_status = form.exchange_status.data
            current_issue.janome_status = form.janome_status.data
            current_issue.comment = form.comment.data
            current_issue.customer_delivery_time = form.customer_delivery_time.data
            current_issue.delivery_time = form.delivery_time.data
            db.session.commit()
            flash('Zmiany zostały zapisane')
            return redirect(url_for('issues'))
        elif request.method == 'GET':
            form.owner.data = current_issue.owner
            form.machine_name.data = current_issue.machine_model
            form.serial_number.data = current_issue.serial_number
            form.part_number.data = current_issue.part_number
            form.quantity.data = current_issue.quantity
            form.part_name.data = current_issue.part_name
            form.issue_desc.data = current_issue.issue_desc
            form.where_is_part.data = current_issue.where_is_part
            form.exchange_status.data = current_issue.exchange_status
            form.janome_status.data = current_issue.janome_status
            form.comment.data = current_issue.comment
            form.customer_delivery_time.data = current_issue.customer_delivery_time
            form.delivery_time.data = current_issue.delivery_time

        return render_template(
            'edit_issue.html', issue_id=issue_id, title='Edytycja zgłoszenia', form=form, machines_list=machines_list, current_issue=current_issue)
    else:
        return redirect(url_for('index'))#nieuprawniony dostęp


@app.route('/add_user/', methods=['GET', 'POST'])
def add_user():
    pass

@app.route('/edit_user/', methods=['GET', 'POST'])
def edit_user():
    pass

@app.route('/add_machine/', methods=['GET', 'POST'])
@login_required
#add new machine for db
def add_machine():
    if current_user.user_type == 'admin':
        form = NewMachineForm()
        machine_list = Machines.query.order_by(Machines.name).all()
        if form.validate_on_submit():
            machine = Machines(name=form.machine_name.data)
            db.session.add(machine)
            db.session.commit()
            flash('Dodano maszynę')
            return redirect(url_for('add_machine'))
        if "remove" in request.form:
            machine = request.form.to_dict()
            machine_id = machine['form_machine_id']
            current_machine = Machines.query.filter_by(id=machine_id).first()
            db.session.delete(current_machine)
            db.session.commit()
            flash('Usunięteo maszynę {}'.format(current_machine))
            return redirect(url_for('add_machine'))
        return(render_template('add_machine.html', title="Dodaj maszynę", form=form, machine_list=machine_list))
    else:
        return redirect(url_for('index')) #nieuprawniony dostęp
