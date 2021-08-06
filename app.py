from flask import Flask, render_template, request, make_response, redirect
import pymysql

mysql = pymysql.connect(host='localhost', port=3306,
                        user='root', password='Admin1234', database='db_agenda')

app = Flask(__name__)


@app.route('/')
def index():
    return make_response(redirect('/home'))


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/add_contact', methods=['GET', 'POST'])
def register():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    cur = mysql.cursor(pymysql.cursors.DictCursor)

    cur.execute("INSERT INTO contactos(nombre, telefono, correo) VALUES(%s, %s, %s)",
                (nombre, telefono, correo))
    mysql.commit()
    cur.close()
    return render_template('response.html', nombre=nombre)


@app.errorhandler(404)
def error(error):
    return render_template('error404.html')


if __name__ == '__main__':
    app.run()
