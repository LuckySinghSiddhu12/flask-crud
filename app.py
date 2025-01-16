from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "secret_key"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask_crud'

mysql = MySQL(app)

# Home - Read Data
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

# Create User
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
        mysql.connection.commit()
        flash("User added successfully!")
        return redirect(url_for('index'))
    return render_template('create.html')

# Update User
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        cursor.execute("""
            UPDATE users 
            SET name=%s, email=%s, age=%s 
            WHERE id=%s
        """, (name, email, age, id))
        mysql.connection.commit()
        flash("User updated successfully!")
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    return render_template('update.html', user=user)

# Delete User
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    flash("User deleted successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
