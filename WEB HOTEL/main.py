from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import datetime
import MySQLdb.cursors
import re
import pdfkit
import os

path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

app = Flask(__name__)
# instantiate the mail class
mail = Mail(app)
# Koneksi ke database
app.secret_key = 'test'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uas_python'
mysql = MySQL(app)

# datetime ketika cust booking hotel
now = datetime.datetime.now()

app.config['PDF_FOLDER'] = os.path.realpath('.') + '/static/pdf'
app.config['TEMPLATE_FOLDER'] = os.path.realpath('.') + '/templates'


# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '**************'
app.config['MAIL_PASSWORD'] = '*************'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


# @app.route('/print')
# def print():
#     htmlfile = app.config['TEMPLATE_FOLDER'] + '/test.html'

#     pdffile = app.config['PDF_FOLDER'] + '/laporan.pdf'
#     pdfkit.from_file(htmlfile, pdffile, configuration = config)
#     return '''
#         Proses konversi ke PDF telah berhasil. <br/>
#         Klik <a href="http://localhost:5000/static/pdf/laporan.pdf">click here <a/>
#         untuk membuka file tersebut.
#         '''

# Halaman utama
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html', email=session['email'], username=session['nama'])

    return redirect(url_for('login'))

# proses login user


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM pelanggan WHERE email_pelanggan = %s AND password_pelanggan = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            # session['email'] = account['email']
            session['email'] = account['email_pelanggan']
            # session['username'] = account['nama_pelanggan']
            session['nama'] = account['nama_pelanggan']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    # Show the login form with message (if any)
    return render_template('customer/login.html', msg=msg)

# proses register user


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'password' in request.form and 'username' in request.form and 'email' in request.form:
        # Create variables for easy access
        password = request.form['password']
        email = request.form['email']
        username = request.form['username']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM pelanggan WHERE email_pelanggan = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO pelanggan (email_pelanggan, id_pelanggan, nama_pelanggan, password_pelanggan) VALUES (%s, %s, %s, %s)',
                           (email, '', username, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('customer/register.html', msg=msg)

# proses logout user


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('email', None)
    # session.pop('id', None)
    # Redirect to login page
    return redirect(url_for('login'))

# proses input from booking hotel oleh user


@app.route('/pelanggan-insert', methods=['POST'])
def pelangganInsert():
    if request.method == 'POST':
        username = request.form['username']
        telepon = request.form['telepon']
        jml = request.form['jml']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        tipe = request.form['tipe']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sewa (id_sewa, type_kamar, email_pelanggan, nama, telepon, checkin, checkout, jumlah, tgl_booking) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    ('', tipe, session['email'], username, telepon, checkin, checkout, jml, now))
        mysql.connection.commit()
        return redirect(url_for('home'))

# proses Read data status booking


@app.route('/pelanggan-insert/detail')
def pelangganStatus():
    if 'loggedin' in session:
        email = session['email']
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM sewa WHERE email_pelanggan = %s', (email,))
        datatampil = cur.fetchall()
        cur.close()
        return render_template('status.html', data_sewa=datatampil, username=session['nama'])
    return redirect(url_for('login'))
# Proses login admin dengan session


@app.route('/loginadmin', methods=['GET', 'POST'])
def loginAdmin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM admin WHERE email_admin = %s AND password_admin = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin_admin'] = True
            # session['email'] = account['email']
            session['username'] = account['nama_admin']
            # session['email'] = account['email']
            session['email_admin'] = account['email_admin']
            # Redirect to home page
            return redirect(url_for('adminTampilData'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('admin/login.html', msg=msg)


@app.route('/logoutAdmin')
def logoutAdmin():
    # Remove session data, this will log the user out
    session.pop('loggedin_admin', None)
    session.pop('email_admin', None)
    # session.pop('id', None)
    # Redirect to login page
    return redirect(url_for('loginAdmin'))

# proses Read data admin


@app.route('/admin')
def adminTampilData():
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin ORDER BY nama_admin ASC")
        datatampil = cur.fetchall()
        cur.close()
        return render_template('admin/admin.html', data_admin=datatampil, nama=session['username'])
    return redirect(url_for('loginAdmin'))

# proses delete data admin


@app.route('/hapusadmin/<int:telp>', methods=["GET"])
def deleteAdmin(telp):
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM admin WHERE telepon_admin=%s", (telp,))
        mysql.connection.commit()
        flash("data Berhasil di Hapus")
        return redirect(url_for('adminTampilData'))
    return redirect(url_for('loginAdmin'))

# proses update data admin


@app.route('/admin/updateadmin', methods=['POST'])
def updateAdmin():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            email = request.form['email']
            nama = request.form['nama']
            password = request.form['password']
            telp = request.form['telp']

            cur = mysql.connection.cursor()
            cur.execute("UPDATE admin SET password_admin=%s, nama_admin=%s, telepon_admin=%s WHERE email_admin=%s",
                        (password, nama, telp, email))
            mysql.connection.commit()
            flash("Data Berhasil di Update")
        return redirect(url_for('adminTampilData'))
    return redirect(url_for('loginAdmin'))
# proses input akun oleh admin


@app.route('/admin/inputadmin', methods=['POST'])
def inputAdmin():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            email = request.form['email_admin']
            nama = request.form['nama_admin']
            password = request.form['password_admin']
            telp = request.form['telp_admin']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO admin (email_admin, password_admin, nama_admin, telepon_admin) VALUES (%s, %s, %s, %s)",
                        (email, password, nama, telp))
            mysql.connection.commit()
            flash("Data Berhasil di tambah")
        return redirect(url_for('adminTampilData'))
    return redirect(url_for('loginAdmin'))
# Read data tipe kamar


@app.route('/kamar')
def dataKamar():
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM jenis_kamar ORDER BY type_kamar ASC")
        datatampil = cur.fetchall()
        cur.close()
        return render_template('kamar/kamar.html', data_kamar=datatampil, nama=session['username'])
    return redirect(url_for('loginAdmin'))

# proses delete data kamar


@app.route('/hapuskamar/<int:id>', methods=["GET"])
def deleteKamar(id):
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM jenis_kamar WHERE id=%s", (id,))
        mysql.connection.commit()
        flash("data Berhasil di Hapus")
        return redirect(url_for('dataKamar'))
    return redirect(url_for('loginAdmin'))

# proses update data kamar


@app.route('/kamar/updatekamar', methods=['POST'])
def updateKamar():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            tipe = request.form['tipe']
            stock = request.form['stock']
            harga = request.form['harga']
            id = request.form['id']

            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE jenis_kamar SET stock_kamar=%s, harga_kamar=%s, type_kamar=%s WHERE id=%s", (stock, harga, tipe, id))
            mysql.connection.commit()
            flash("Data Berhasil di Update")
        return redirect(url_for('dataKamar'))
    return redirect(url_for('loginAdmin'))

# proses input kamar oleh admin


@app.route('/kamar/inputkamar', methods=['POST'])
def inputKamar():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            tipe = request.form['tipe']
            stock = request.form['stock']
            harga = request.form['harga']

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO jenis_kamar (type_kamar, stock_kamar, harga_kamar, id) VALUES (%s, %s, %s, %s)", (tipe, stock, harga, ''))
            mysql.connection.commit()
            flash("Data Berhasil di tambah")
        return redirect(url_for('dataKamar'))
    return redirect(url_for('loginAdmin'))
# Read data pelanggan


@app.route('/pelanggan')
def dataPelanggan():
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pelanggan ORDER BY nama_pelanggan ASC")
        datatampil = cur.fetchall()
        email = []

        for i in datatampil:
            email.append(i[0])
        cur.close()
        return render_template('customer/pelanggan.html', data_pelanggan=datatampil, email=email, nama=session['username'])
    return redirect(url_for('loginAdmin'))

# proses delete data pelanggan


@app.route('/hapuspelanggan/<int:id_pelanggan>', methods=["GET"])
def deletePelanggan(id_pelanggan):
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM pelanggan WHERE id_pelanggan=%s",
                    (id_pelanggan,))
        mysql.connection.commit()
        flash("data Berhasil di Hapus")
        return redirect(url_for('dataPelanggan'))
    return redirect(url_for('loginAdmin'))

# proses update data pelanggan


@app.route('/pelanggan/updatepelanggan', methods=['POST'])
def updatePelanggan():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']

            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE pelanggan SET nama_pelanggan=%s, password_pelanggan=%s WHERE email_pelanggan=%s", (name, password, email))
            mysql.connection.commit()
            flash("Data Berhasil di Update")
        return redirect(url_for('dataPelanggan'))
    return redirect(url_for('loginAdmin'))
# proses input cust oleh admin


@app.route('/pelanggan/inputpelanggan', methods=['POST'])
def inputPelanggan():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO pelanggan (email_pelanggan, id_pelanggan, nama_pelanggan, password_pelanggan) VALUES (%s, %s, %s, %s)",
                        (email, '', name, password))
            mysql.connection.commit()
            flash("Data Berhasil di tambah")
        return redirect(url_for('dataPelanggan'))
    return redirect(url_for('loginAdmin'))
# send blast email


@app.route("/pelanggan/mail", methods=['GET', 'POST'])
def mail():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            subject = request.form['subject']
            msg = request.form['msg']

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM pelanggan")
            datatampil = cur.fetchall()
            cur.close()
            email = []

            for i in datatampil:
                email.append(i[0])
            cur.close()

            pesan = Message(subject, sender='wannanoob@gmail.com',
                            recipients=email)
            pesan.body = msg

            try:
                mail = Mail(app)
                mail.connect()
                mail.send(pesan)
                return render_template('mail/success.html')
            except:
                return render_template('mail/error.html')

        return redirect(url_for('dataPelanggan'))
    return redirect(url_for('loginAdmin'))

# @app.route("/pelanggan/mail")
# def mail():
#     msg = Message(
#         'Hello',
#         sender='tugasyubiem@gmail.com',
#         recipients=['jericho.kecil@gmail.com']
#     )
#     msg.body = 'Hello Flask message sent from Flask-Mail'
#     mail.send(msg)
#     return 'Sent'

# Read data sewa


@app.route('/sewa')
def dataSewa():
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sewa ORDER BY id_sewa")
        datatampil = cur.fetchall()
        cur.close()
        return render_template('sewa/sewa.html', data_sewa=datatampil, nama=session['username'])
    return redirect(url_for('loginAdmin'))

# proses delete data sewa


@app.route('/hapussewa/<int:id_sewa>', methods=["GET"])
def deleteSewa(id_sewa):
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM sewa WHERE id_sewa=%s", (id_sewa,))
        mysql.connection.commit()
        flash("data Berhasil di Hapus")
        return redirect(url_for('dataSewa'))
    return redirect(url_for('loginAdmin'))

# proses update data sewa


@app.route('/sewa/updatesewa', methods=['POST'])
def updateSewa():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            id = request.form['id']
            tipe = request.form['tipe']
            email = request.form['email']
            nama = request.form['nama']
            telp = request.form['telp']
            checkin = request.form['checkin']
            checkout = request.form['checkout']
            jumlah = request.form['jumlah']
            status = request.form['status']

            cur = mysql.connection.cursor()
            cur.execute("UPDATE sewa SET type_kamar=%s, email_pelanggan=%s, nama=%s, telepon=%s, checkin=%s, checkout=%s, jumlah=%s, status=%s WHERE id_sewa=%s",
                        (tipe, email, nama, telp, checkin, checkout, jumlah, status, id))
            mysql.connection.commit()
            flash("Data Berhasil di Update")
        return redirect(url_for('dataSewa'))
    return redirect(url_for('loginAdmin'))
# proses input sewa hotel oleh admin


@app.route('/sewa/inputsewa', methods=['POST'])
def inputSewa():
    if 'loggedin_admin' in session:
        if request.method == 'POST':
            tipe = request.form['tipe']
            email = request.form['email']
            nama = request.form['nama']
            telp = request.form['telp']
            checkin = request.form['checkin']
            checkout = request.form['checkout']
            jumlah = request.form['jumlah']
            status = request.form['status']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO sewa (id_sewa, type_kamar, email_pelanggan, nama, telepon, checkin, checkout, jumlah, status, tgl_booking) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        ('', tipe, email, nama, telp, checkin, checkout, jumlah, status, now))
            mysql.connection.commit()
            return redirect(url_for('dataSewa'))
    return redirect(url_for('loginAdmin'))
# proses Print laporan sewa


@app.route('/sewa/print')
def print():
    if 'loggedin_admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sewa")
        datatampil = cur.fetchall()
        id_sewa = []
        jenis = []
        email = []
        nama = []
        telp = []
        checkin = []
        checkout = []
        book = []
        jumlah = []
        status = []

        for i in datatampil:
            id_sewa.append(i[0])
            jenis.append(i[1])
            email.append(i[2])
            nama.append(i[3])
            telp.append(i[4])
            checkin.append(i[5])
            checkout.append(i[6])
            book.append(i[9])
            jumlah.append(i[7])
            status.append(i[8])
        cur.close()

        try:
            rendered = render_template('sewa/laporanSewa.html', data_admin=datatampil, id_sewa=id_sewa, jenis=jenis, email=email,
                                       nama=nama, telp=telp, checkin=checkin, checkout=checkout, book=book, jumlah=jumlah, status=status)
            pdf = pdfkit.from_string(rendered, configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'inline; filename= laporan_sewa.pdf'
            return response
        except:
            return render_template('mail/pdferror.html')
    return redirect(url_for('loginAdmin'))


if __name__ == '__main__':
    app.run(debug=True)
