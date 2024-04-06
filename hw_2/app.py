# Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан
# cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия, где будет
# отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными
# пользователя и произведено перенаправление на страницу ввода имени и электронной почты.


from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def set_name():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        response = make_response(redirect('/welcome'))
        response.set_cookie('username', name)
        response.set_cookie('email', mail)
        return response
    return render_template('set_name.html')


@app.route('/welcome')
def welcome():
    name = request.cookies.get('username')
    mail = request.cookies.get('email')
    return render_template('welcome.html', name=name, mail=mail)


@app.route('/del_cookie', methods=['POST'])
def del_cookie():
    response = make_response(redirect('/'))
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


if __name__ == '__main__':
    app.run(debug=True)
