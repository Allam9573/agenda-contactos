from flask import Flask, render_template, request, make_response, redirect
import mysql.connector

mysql = mysql.connector.connect(host='localhost',
                        user='root', password='admin1234', database='db_agenda')

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
    cursor = mysql.cursor(buffered=True)

    cursor.execute("INSERT INTO contactos(nombre, telefono, correo) VALUES(%s, %s, %s)",
                (nombre, telefono, correo)  )
    mysql.commit()
    cursor.close()
    return render_template('response.html', nombre=nombre)


@app.route('/mis_contactos')
def getContactos():
    cursor = mysql.cursor(dictionary=True)
    cursor.execute('SELECT * FROM contactos')
    data = cursor.fetchall()
    return render_template('miscontactos.html', contacts=data, title='Mis Contactos')


@app.route('/delete_contact/<id_user>')
def delete(id_user):
    id_user = int(id_user)
    cursor = mysql.cursor(buffered=True)
    query = f'DELETE FROM contactos WHERE id_contacto = {id_user}'
    cursor.execute(query)
    mysql.commit()
    cursor.close()
    return make_response(redirect('/mis_contactos'))

@app.route('/edit_contact/<id>')
def edit_contact(id):
    cursor = mysql.cursor(dictionary=True)
    cursor.execute('SELECT * FROM contactos WHERE id_contacto=%s', [id])
    data=cursor.fetchone()
    return render_template('edit_contact.html', data=data, title='Editar Contacto')

@app.route('/update/', methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cursor = mysql.cursor(buffered=True)
        cursor.execute("UPDATE contactos set nombre=%s, telefono=%s, correo=%s WHERE id_contacto=%s",(nombre,telefono,correo,id))
        mysql.commit()
    return redirect('/mis_contactos')
    

@app.errorhandler(404)
def error(error):
    return render_template('error404.html')


if __name__ == '__main__':
    app.run()
    