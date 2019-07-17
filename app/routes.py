from flask import render_template, flash, redirect, url_for, request, Response, send_file, session
from werkzeug.urls import url_parse
from app import app, db, email, payments_mod, events
from app.forms import LoginForm, IssueForm, EditIssueForm, UserForm, NewMachineForm, UserEditForm, DelayedPaymentsForm, CustomerForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Issues, Machines, Customers
from pandas import DataFrame


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
#strona główna z niezakończonymi zgłoszeniami, dla danego użytkownika [PL]
    if current_user.user_type in ('admin', 'warehouse', 'office'):
        page = request.args.get('page', 1, type=int)
        issues = Issues.query.filter(~Issues.janome_status.in_(['wymienione', 'odrzucone'])).order_by(Issues.time_stamp.desc()).paginate(
            page, app.config['ISSUES_PER_PAGE'], False)
        next_url = url_for('issues', page=issues.next_num) if issues.has_next else None
        prev_url = url_for('issues', page=issues.prev_num) if issues.has_prev else None

    elif current_user.user_type in ('service'):
        page = request.args.get('page', 1, type=int)
        issues = Issues.query.filter(Issues.owner == current_user.username,  ~Issues.janome_status.in_(['wymienione', 'odrzucone'])).order_by(Issues.time_stamp.desc()).paginate(
            page, app.config['ISSUES_PER_PAGE'], False)
        next_url = url_for('issues', page=issues.next_num) if issues.has_next else None
        prev_url = url_for('issues', page=issues.prev_num) if issues.has_prev else None

    if 'edit' in request.form:
        issue = request.form.to_dict()
        issue_id = issue['form_id']
        return redirect(url_for('edit_issue', issue_id=issue_id))
    if 'remove' in request.form:
        issue = request.form.to_dict()
        issue_id = issue['form_id']
        selected_issue = Issues.query.filter_by(id=issue_id).first()
        db.session.delete(selected_issue)
        db.session.commit()
        flash('Zgłoszenie nr {} zostało usunięte'.format(issue_id))
        events.events_rec(current_user.username, 'issue {} was removed'.format(issue_id))
        return redirect(url_for('index'))
    if "export" in request.form:
        #wywalić do osobnego modułu dodać do zgłoszeń
        col0 = []
        col1 = []
        col2 = []
        col3 = []
        col4 = []
        col5 = []
        col6 = []
        issues = Issues.query.filter(Issues.janome_status.in_(['niezgłoszone']))
        issues_id_list = []
        for item in issues:
            col0.append(item.id)
            col1.append(item.machine_model)
            col2.append(item.serial_number)
            col3.append(item.part_number)
            col4.append(item.quantity)
            col5.append(item.part_name)
            col6.append(item.issue_desc)
            issues_id_list.append(item.id)
        df = DataFrame({'Id.': col0,
                        'Machine model': col1,
                        'Serial number': col2,
                        'Part number': col3,
                        'Qty': col4,
                        'Part name': col5,
                        'Issue desc.': col6
                        })
        events.events_rec(current_user.username, 'export xlsx file for these isuess id: {}'.format(''.join(str(issues_id_list))))
        #online:
        df.to_excel(r'/home/eaters/mysite/app/static/waranty_parts_XX.XX.XXXX.xlsx', sheet_name='waranty_parts1', index=False)
        return send_file(r'/home/eaters/mysite/app/static/waranty_parts_XX.XX.XXXX.xlsx',attachment_filename='waranty_parts_XX.XX.XXXX.xlsx', as_attachment=True)
        #offline:
        #df.to_excel(r'app\raports\waranty_parts_XX.XX.XXXX.xlsx', sheet_name='waranty_parts1', index=False)
        #return send_file(r'raports\waranty_parts_XX.XX.XXXX.xlsx',attachment_filename='waranty_parts_XX.XX.XXXX.xlsx', as_attachment=True)

    if "set_done" in request.form:
        new_issues = Issues.query.filter(Issues.janome_status.in_(['niezgłoszone', 'Niezgłoszone']))
        for item in new_issues:
            item.janome_status = 'zgłoszone'
            db.session.commit()
            description = 'changed janome status for "zgłoszone" for {} issue'.format(item.id)
            events.events_rec(current_user.username, description)
        return redirect(url_for('index'))
    return render_template('index.html', issues=issues.items, title='Strona główna', version=app.config['VERSION'], next_url=next_url, prev_url=prev_url)

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
        events.events_rec(current_user.username, 'was logged in')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Logowanie', form=form, version=app.config['VERSION'])

@app.route('/logout/')
def logout():
    events.events_rec(current_user.username, 'was logged out')
    logout_user()
    return redirect(url_for('index'))

@app.route('/issues/', methods=['GET','POST'])
@login_required
def issues():
#is showing the list of issues
    if current_user.user_type in ('admin', 'warehouse', "office"):
        page = request.args.get('page', 1, type=int)
        issues = Issues.query.order_by(Issues.time_stamp.desc()).paginate(
            page, app.config['ISSUES_PER_PAGE'], False)
        next_url = url_for('issues', page=issues.next_num) if issues.has_next else None
        prev_url = url_for('issues', page=issues.prev_num) if issues.has_prev else None
    elif current_user.user_type in ('service'):
        page = request.args.get('page', 1, type=int)
        issues = Issues.query.filter(Issues.owner == current_user.username).order_by(Issues.time_stamp.desc()).paginate(
            page, app.config['ISSUES_PER_PAGE'], False)
        next_url = url_for('issues', page=issues.next_num) if issues.has_next else None
        prev_url = url_for('issues', page=issues.prev_num) if issues.has_prev else None
    if 'edit' in request.form:
        issue = request.form.to_dict()
        issue_id = issue['form_id']
        return redirect(url_for('edit_issue', issue_id=issue_id))
    if 'remove' in request.form:
        issue = request.form.to_dict()
        issue_id = issue['form_id']
        selected_issue = Issues.query.filter_by(id=issue_id).first()
        db.session.delete(selected_issue)
        db.session.commit()
        flash('Zgłoszenie nr {} zostało usunięte'.format(issue_id))
        events.events_rec(current_user.username, 'issue {} was removed'.format(issue_id))
        return redirect(url_for('issues'))
    return render_template('index.html', issues=issues.items, title='Zgłoszenia', next_url=next_url, prev_url=prev_url, version=app.config['VERSION'])


@app.route('/new_issue/', methods = ['GET', 'POST'])
@login_required
def new_issue():
    machines_list = Machines.query.order_by(Machines.name).all()
    form = IssueForm()
    form.owner.data = current_user.username
    if form.validate_on_submit():
        issue = Issues(
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
        flash('Dodano zgłoszenie nr {}'.format(issue.id))
        events.events_rec(current_user.username, 'added: {}'.format(str(issue)))
        #online:
        email.send_new_issue(current_user, issue)
        return redirect(url_for('issues'))
    return render_template('/new_issue.html', title='Nowe zgłoszenie', form=form, machines_list=machines_list, version=app.config['VERSION'])

@app.route('/edit_issue/<issue_id>', methods=['GET', 'POST'])
@login_required
def edit_issue(issue_id):
    current_issue = Issues.query.filter_by(id=issue_id).first()
    machines_list = Machines.query.order_by(Machines.name).all()
    form = EditIssueForm()
    if (current_user.username == current_issue.owner) or current_user.user_type in ("admin", "warehouse", "office"):
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
            events.events_rec(current_user.username, 'edit: {}'.format(str(current_issue)))
            return redirect(url_for('index'))
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
            'edit_issue.html', issue_id=issue_id, title='Edytycja zgłoszenia', form=form, machines_list=machines_list, current_issue=current_issue, version=app.config['VERSION'])
    else:
        return render_template('access_denied.html', title='Brak dostępu')


@app.route('/users/', methods=['GET', 'POST'])
@login_required
# add, remove or go to edit site for all users
def users():
    users_type_list = ['admin', 'warehouse', 'service', 'office', '']
    users = User.query.order_by(User.username).all()
    if current_user.user_type == 'admin':
        form = UserForm()
        if form.validate_on_submit():
            user = User(
            username=form.username.data,
            email=form.email.data,
            user_type=request.form.get('user_type')
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Dodano nowego użytkownika')
            events.events_rec(current_user.username, 'added new user: {}'.format(user.username))
            return redirect(url_for('users'))
        if "remove" in request.form:
            user = request.form.to_dict()
            user_id = user['form_user_id']
            selected_user = User.query.filter_by(id=user_id).first()
            db.session.delete(selected_user)
            db.session.commit()
            flash('Usunięto użytkownika {}'.format(selected_user))
            events.events_rec(current_user.username, 'removed user: {}'.format(selected_user.username))
            return redirect(url_for('users'))
        if "edit" in request.form:
            user = request.form.to_dict()
            user_id = user['form_user_id']
            return redirect(url_for('edit_user', user_id=user_id))
    return render_template('/users.html', title='Uzytkownicy', form=form, users_type_list=users_type_list, users=users, version=app.config['VERSION'])

@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
@login_required
#edit users
def edit_user(user_id):
    users_type_list = ['admin', 'warehouse', 'service', 'office', '']
    form = UserEditForm()
    #if current_user.user_type == 'admin':
    if (current_user.id == int(user_id)) or (current_user.user_type == "admin"):
        selected_user = User.query.filter_by(id=user_id).first()
        if form.validate_on_submit():
            selected_user.user_type = form.user_type.data
            selected_user.username = form.username.data
            selected_user.email = form.email.data
            if form.password.data != '' and form.password2.data != '':
                selected_user.set_password(form.password.data)
            db.session.commit()
            flash('Zmiany zostały zapisane')
            events.events_rec(current_user.username, 'changed user data: {}'.format(str(selected_user)))
            if current_user.user_type in "admin":
                return redirect(url_for('users'))
            else:
                return(redirect(url_for('index')))
        elif request.method == 'GET':
            form.user_type.data = selected_user.user_type
            form.username.data = selected_user.username
            form.email.data = selected_user.email
    else:
        flash('Twoje id {} nie jest równe {}'.format(current_user.id, user_id))
        events.events_rec(current_user.username, 'tried tricky tricks :)')
        return redirect(url_for('index'))#nieuprawniony dostęp
    return render_template('/edit_user.html', title = 'Edycja konta użytkownika',
    form=form, users_type_list=users_type_list, user_id=user_id, selected_user=selected_user, version=app.config['VERSION'])


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
            events.events_rec(current_user.username, 'added new machine: {}'.format(machine.name))
            return redirect(url_for('add_machine'))
        if "remove" in request.form:
            machine = request.form.to_dict()
            machine_id = machine['form_machine_id']
            current_machine = Machines.query.filter_by(id=machine_id).first()
            db.session.delete(current_machine)
            db.session.commit()
            flash('Usunięteo maszynę {}'.format(current_machine))
            events.events_rec(current_user.username, 'removed: {}'.format(current_machine.name))
            return redirect(url_for('add_machine'))
        return(render_template('add_machine.html', title="Dodaj maszynę", form=form, machine_list=machine_list, version=app.config['VERSION']))
    else:
        return render_template('access_denied.html', title='Brak dostępu')

@app.route('/payments/', methods=['GET','POST'])
@login_required
def payments():
    form = DelayedPaymentsForm()
    if current_user.user_type in ('admin', "office"):
        delayed_dict = {}
        if form.validate_on_submit():
            data = form.clipboard_data.data
            delayed_dict = payments_mod.delayed_payments(data)
            session["delayed_dict"] = delayed_dict
        if "send_to_all" in request.form:
            delayed_dict = session["delayed_dict"]
            for customer_code in delayed_dict.keys():
                try:
                    selected_customer = Customers.query.filter_by(code=customer_code).first()
                    data = delayed_dict[customer_code]
                    email.send_delayed_payments(selected_customer, data)
                    flash('Wysłano do {}'.format(customer_code))
                    events.events_rec(current_user.username,'sended mail to {}'.format(customer_code))
                except:
                    flash('Nie udało się wysłać do {}'.format(customer_code))
            session["delayed_dict"] = {}

        if "remove" in request.form:
            delayed_dict = session["delayed_dict"]
            request_data = request.form.to_dict()
            selected_customer = request_data['form_delayed_dict']
            del delayed_dict[selected_customer]
            session["delayed_dict"] = delayed_dict
        if "send" in request.form:
            try:
                delayed_dict = session["delayed_dict"]
                request_data = request.form.to_dict()
                selected_customer_code = request_data['form_delayed_dict']
                selected_customer = Customers.query.filter_by(code=selected_customer_code).first()
                email.send_delayed_payments(selected_customer, delayed_dict[selected_customer_code])
                del delayed_dict[selected_customer_code]
                session["delayed_dict"] = delayed_dict
                flash('Wysłano do {}'.format(selected_customer_code))
                events.events_rec(current_user.username, 'sended mail to {}'.format(selected_customer_code))
            except:
                flash('Nie udało się wysłać do {}'.format(selected_customer_code))

        return (render_template('payments.html', title='Płatności', form=form, delayed_dict=delayed_dict, version=app.config['VERSION']))
    else:
        return render_template('access_denied.html', title='Brak dostępu')
@app.route('/customers/', methods =['GET', 'POST'])
@login_required
def customers():
    form = CustomerForm()
    if current_user.user_type in ('admin', "office"):
        customers_list = Customers.query.order_by(Customers.code).all()
        if form.validate_on_submit():
            new_customer = Customers(
                code=form.code.data,
                name=form.name.data,
                email=form.email.data,
                phone_num=form.phone_num.data,
                phone2_num=form.phone2_num.data,
            )
            db.session.add(new_customer)
            db.session.commit()
            flash('Dodano klienta {}'.format(new_customer.code))
            events.events_rec(current_user.username, 'added new customer: {} with mail: {}'.format(new_customer.code, new_customer.email))
            return redirect(url_for('customers'))
        if "remove" in request.form:
            customer = request.form.to_dict()
            customer_id = customer['form_customer_id']
            selected_customer = Customers.query.filter_by(id=customer_id).first()
            db.session.delete(selected_customer)
            db.session.commit()
            flash('Usunięto klienta {}'.format(selected_customer.code))
            events.events_rec(current_user.username, 'removed customer: {}'.format(selected_customer.code))
            return redirect(url_for('customers'))
        if "edit" in request.form:
            customer = request.form.to_dict()
            customer_id = customer['form_customer_id']
            return redirect(url_for('edit_customer', customer_id=customer_id))
            pass

    return render_template('customers.html', title='Klienci', form=form, customers=customers_list, version=app.config['VERSION'])

@app.route('/edit_customer/<customer_id>', methods = ['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    form = CustomerForm()
    if current_user.user_type in ('admin', 'office'):
        selected_customer = Customers.query.filter_by(id=customer_id).first()
        if form.validate_on_submit():
            selected_customer.code = form.code.data
            selected_customer.name = form.name.data
            selected_customer.email = form.email.data
            selected_customer.phone_num = form.phone_num.data
            selected_customer.phone2_num = form.phone2_num.data
            db.session.commit()
            flash('Zmiany zostały zapisane')
            events.events_rec(current_user.username, 'edited customer: {}'.format(str(selected_customer)))
            return redirect(url_for('customers'))
        elif request.method == 'GET':
            form.code.data = selected_customer.code
            form.name.data = selected_customer.name
            form.email.data = selected_customer.email
            form.phone_num.data = selected_customer.phone_num
            form.phone2_num.data = selected_customer.phone2_num
    else:
        return render_template('access_denied.html', title='Brak dostępu')
    return render_template('/edit_customer.html', title='Edycja klienta', form=form, customer_id=customer_id, selected_customer=selected_customer, version=app.config['VERSION'])
