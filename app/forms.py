from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import Machines

class LoginForm(FlaskForm):
    username = StringField('Użytkownik', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')

class IssueForm(FlaskForm):
    #machines_list = ['','JANOME MB-4', 'JANOME MB-7', 'JUNO E1015'] - toremove
    owner = StringField('Zgłaszajacy: ', validators=[DataRequired()])
    machine_name = StringField('Model maszyny: ')#, choices=machines_list)#, validators=[DataRequired()])
    serial_number = StringField('Numer seryjny: ', validators=[DataRequired()])
    part_number = StringField('Numer części: ', validators=[DataRequired()])
    part_name = StringField('Nazwa częśći (angielska z listy części): ')
    issue_desc = TextAreaField('Opis usterki: ', validators=[DataRequired(), Length(min=3, max=400)])
    submit = SubmitField('Wyślij zgłoszenie')

class EditIssueForm(IssueForm):
    quantity = IntegerField('Ilość:')
    where_is_part = StringField('Status dostarczenia do magazynu: ')
    exchange_status = StringField('Status wymiany klientowi: ')
    janome_status = StringField('Status zgłoszenia w Janome: ')
    customer_delivery_time = StringField('Dostawa do klienta: ')
    delivery_time = StringField('Dostawa so ETI: ')
    comment = TextAreaField('Uwagi: ')
    submit = SubmitField('Zapisz zmiany')

class UserForm(FlaskForm):
    user_type = StringField('Typ użytkownika', validators=[DataRequired()])
    username = StringField('Nazwa użytkownika:', validators=[DataRequired()])
    email = StringField('Email:',validators=[DataRequired()])
    password = PasswordField('Hasło:', validators=[DataRequired()])
    password2 = PasswordField('Powtórz hasło:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zapisz')

    def validate_user_name(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Uzytkownik o takiej nazwie już istnieje.')

class UserEditForm(UserForm):
    password = PasswordField('Hasło:')
    password2 = PasswordField('Powtórz hasło:', validators=[EqualTo('password')])

class NewMachineForm(FlaskForm):
    machine_name = StringField('Model maszyny:')
    submit = SubmitField('Zapisz')

    def validate_machine_name(self, machine_name):
        machine = Machines.query.filter_by(name=machine_name.data).first()
        if machine is not None:
            raise ValidationError('Ten model maszyny jest już w bazie.')

class DelayedPaymentsForm(FlaskForm):
    clipboard_data = TextAreaField('Dane z symfonii:', validators=[DataRequired()])
    submit = SubmitField('Przetwarzaj')
