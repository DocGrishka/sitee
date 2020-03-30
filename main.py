from flask import *
import sys

from flask_login import login_manager, login_user, login_required, LoginManager, logout_user
from wtforms.fields.html5 import EmailField
from data.db_session import global_init
from data.db_session import create_session
from data.user_info import User
from data.tovar_info import Product
from data.Manufactures import Manufacture
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import TextField, PasswordField, IntegerField, validators, SelectField

app = Flask(__name__)
app.config["SECRET_KEY"] = 'sssddddwy'
global_init('db/shop.db')
login_manager = LoginManager()
login_manager.init_app(app)

MASS = [('1', 'Samsung'), ('2', 'Sony')]
session_db = create_session()


class RegisterForm(FlaskForm):
    login = EmailField('Ваш логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    email = EmailField('Ваша почта', validators=[DataRequired()])
    telephone = StringField('Телефон для подтверждения заказа', validators=[DataRequired()])

    submit = SubmitField('Submit')


class AddTowar(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    Count = IntegerField('Количество', validators=[DataRequired()])
    Price = StringField('Цена', validators=[DataRequired()])
    Manufacture = SelectField('Производитель', choices=MASS, coerce=int)
    submit = SubmitField('Добавить')


class Adddev(FlaskForm):
    Company = StringField('Название компании', validators=[DataRequired()])
    Town = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class LoginForm(FlaskForm):
    username = StringField('Ваш логин', validators=[DataRequired()])
    password = PasswordField('Пароль ', validators=[DataRequired()])
    submit = SubmitField('Войти')
    remember_me = BooleanField('Запомнить меня')


@app.route('/add_dev', methods=['GET', 'POST'])
def add():
    data = [(i.name, i.Price, session_db.query(Manufacture).filter(Manufacture.id == i.Manufacture).first().Company) for
            i in session_db.query(Product)]
    if 'admin' in session:
        if session['admin'] != 1:
            return render_template('index.html', title='Аварийный доступ', list_data=data,
                                   n=len(session_db.query(Product).all()))
    else:
        return render_template('index.html', title='Аварийный доступ', list_data=data,
                               n=len(session_db.query(Product).all()))
    # session = create_session()
    #
    lis = [('Кулька', 'Булька'), ('Кулька2', 'Булька2')]
    form = Adddev()
    if form.validate_on_submit():
        man = Manufacture(
            Company=form.Company.data,
            Town=form.Town.data
        )
        session_db.add(man)
        session_db.commit()
        return redirect('/')
    return render_template('add_developer.html', title='Добавление', form=form)


@app.route('/add_tow', methods=['GET', 'POST'])
def adds():
    data = [(i.name, i.Price, session_db.query(Manufacture).filter(Manufacture.id == i.Manufacture).first().Company) for
            i in session_db.query(Product)]
    if 'admin' in session:
        if session['admin'] != 1:
            return render_template('index.html', title='Аварийный доступ', list_data=data,
                                   n=len(session_db.query(Product).all()))
    else:
        return render_template('index.html', title='Аварийный доступ', list_data=data,
                               n=len(session_db.query(Product).all()))
    # session = create_session()
    form = AddTowar()
    form.Manufacture.choices = ([(i.id, i.Company) for i in session_db.query(Manufacture).all()])
    if form.validate_on_submit():
        towar = Product(
            name=form.name.data,
            Count=form.Count.data,
            Price=form.Price.data,
            Manufacture=form.Manufacture.data
        )
        session_db.add(towar)
        session_db.commit()
        return redirect('/')
    return render_template('add_towar.html', title='Добавление', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        try:
            if int(form.age.data) < 0:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message='Возраст должен быть не меньше 0')
        except BaseException:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Неправильный возраст')
        session_db = create_session()
        if session_db.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            surname=form.surname.data,
            address=form.address.data,
            telephone=form.telephone.data
        )
        user.set_password(form.password.data)
        session_db.add(user)
        session_db.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session_db = create_session()
    return session_db.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session_db = create_session()
        user = session_db.query(User).filter(User.login == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            session['admin'] = user.admin
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/thank')
def thank():
    return render_template('thank_you.html', title='Ваш заказ обрабатывается')


@app.route('/')
def main():
    global MASS

    data = [(i.name, i.Price, session_db.query(Manufacture).filter(Manufacture.id == i.Manufacture).first().Company) for
            i
            in session_db.query(Product)]
    return render_template('index.html', title='Аварийный доступ', list_data=data,
                           n=len(session_db.query(Product).all()))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['admin'] = 0
    return redirect("/")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
