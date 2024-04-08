# Создать форму для регистрации пользователей на сайте. Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль"
# и кнопку "Зарегистрироваться". При отправке формы данные должны сохраняться в базе данных, а пароль должен быть
# зашифрован.


from flask import Flask, render_template, request, flash
from flask_wtf import CSRFProtect
from model import db, User
from form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        email = form.email.data
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!', 'success')
        return render_template('register.html', form=form)

    return render_template('register.html', form=form)


@app.cli.command('create')
def create_db():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
