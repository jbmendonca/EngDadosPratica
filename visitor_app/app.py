import os
from flask import Flask, render_template, request, redirect, session, url_for
import qrcode
import pyodbc

app = Flask(__name__)
app.secret_key = 'change-me'

# Configure SQL Server connection
CONN_STR = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;DATABASE=VisitorDB;UID=sa;PWD=your_password'
)

def get_conn():
    return pyodbc.connect(CONN_STR)

# ---------- User management ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO Users(username, password, role) VALUES(?,?,?)',
                (username, password, role)
            )
            conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT role FROM Users WHERE username=? AND password=?', (username, password))
            row = cursor.fetchone()
            if row:
                session['user'] = username
                session['role'] = row[0]
                return redirect(url_for('visitor_form'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------- Visitor registration ----------
@app.route('/visitor', methods=['GET', 'POST'])
def visitor_form():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        cpf = request.form['cpf']
        phone = request.form['phone']
        sector = request.form['sector']
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO Visitors(name, cpf, phone, sector) VALUES(?,?,?,?)',
                (name, cpf, phone, sector)
            )
            conn.commit()
            visitor_id = cursor.execute('SELECT SCOPE_IDENTITY()').fetchone()[0]
        qr_filename = f'{visitor_id}.png'
        qr_path = os.path.join('static', 'qrcodes', qr_filename)
        img = qrcode.make(f'Visitante:{name};Setor:{sector}')
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        img.save(qr_path)
        visitor = {
            'name': name,
            'sector': sector
        }
        return render_template('visitor_label.html', visitor=visitor, qr_filename=qr_filename)
    return render_template('visitor_form.html')

if __name__ == '__main__':
    app.run(debug=True)
