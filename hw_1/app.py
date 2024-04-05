from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base_template.html')


@app.route('/jacket/')
def jacket():
    return render_template('jacket.html')


@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')


@app.route('/clothes/')
def cloth():
    return render_template('clothes.html')


if __name__ == '__main__':
    app.run()
