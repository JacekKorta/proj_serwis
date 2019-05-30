from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Użytkownik', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')

class IssueForm(FlaskForm):
    machines_list = ['','JANOME MB-4', 'JANOME MB-7', 'JUNO E1015']
    owner = StringField('Zgłaszajacy:', validators=[DataRequired()])
    machine_name = StringField('Model maszyny:')#, choices=machines_list)#, validators=[DataRequired()])
    serial_number = StringField('Numer seryjny:', validators=[DataRequired()])
    part_number = StringField('Numer części:', validators=[DataRequired()])
    part_name = StringField('Nazwa częśći (angielska z listy części):')
    issue_desc = TextAreaField('Opis usterki:', validators=[DataRequired(), Length(min=3, max=400)])
    submit = SubmitField('Wyślij zgłoszenie')

class EditIssueForm(IssueForm):
    quantity = IntegerField('Ilość:')
    where_is_part = StringField('Status dostarczenia do magazynu:')
    exchange_status = StringField('Status wymiany klientowi')
    janome_status = StringField('Status zgłoszenia w Janome')
    customer_delivery_time = StringField('Dostawa do klienta')
    delivery_time = StringField('Dostawa so ETI')
    comment = StringField('Uwagi')
    submit = SubmitField('Zapisz zmiany')
