from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from operator import itemgetter
from types import NoneType

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/', methods=('GET', 'POST'))
def home_page():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'password2' in request.form:
            user_name = request.form['username']
            password = request.form['password']
            password2 = request.form['password2']

            if not user_name or not password or not password2:
                flash("There cannot be empty values", "warning")
                return render_template("index.html")

            if password != password2:
                flash("Two password must be same", "warning")
                return render_template("index.html")

            connection = get_db_connection()

            if connection is None:
                flash("Connection Failed", "danger")
                return render_template("index.html")
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("INSERT INTO users(user_name, user_password) VALUES(%s,%s)", (user_name, password))
                connection.commit()
                flash("Registered Successfully", "success")
                return redirect(url_for('game_page'))
            except Error:
                flash(f"Same Username exists!", "danger")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        elif 'username_delete' in request.form and 'password_delete' in request.form:
            user_name = request.form['username_delete']
            password = request.form['password_delete']
            print(user_name, password)

            connection = get_db_connection()
            if connection is None:
                flash("Connection Failed", "danger")
                return render_template("index.html")

            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_name=%s;", (user_name,))
            the_user = cursor.fetchone()
            print(the_user)

            if type(the_user) is NoneType:
                flash("Username does not exist", "warning")
                cursor.close()
                connection.close()
                return render_template("index.html")

            if the_user.get('user_password') != password:
                flash("Wrong Password", "warning")
                cursor.close()
                connection.close()
                return render_template("index.html")

            cursor.execute("DELETE FROM users WHERE user_name=%s", (user_name,))
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('home_page'))

        elif 'username_login' in request.form and 'password_login' in request.form:
            user_name = request.form['username_login']
            password = request.form['password_login']
            print(user_name, password)

            if not user_name or not password:
                flash("There cannot be empty values", "warning")
                return render_template("index.html")

            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_name=%s;", (user_name,))
            the_user = cursor.fetchone()
            print(the_user)

            if type(the_user) is NoneType:
                flash("Username does not exist", "warning")
                cursor.close()
                connection.close()
                return render_template("index.html")

            if the_user.get('user_password') != password:
                flash("Wrong Password", "warning")
                cursor.close()
                connection.close()
                return render_template("index.html")
            cursor.close()
            connection.close()

            return game_page(user_name)

    return render_template("index.html")


@app.route('/tables')
def tables_page():
    connection = get_db_connection()
    if connection is None:
        flash("Couldn't connect to the database!", "danger")
        return render_template("tables.html", users=[])

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select * from users")
        users = cursor.fetchall()
    except Error as e:
        flash(f"Query failed: {e}", "danger")
        users = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    users = sorted(users, key=itemgetter('high_score'))

    return render_template("tables.html", users=users)


@app.route('/game')
def game_page(username="LOGIN REQUIRED"):
    return render_template("game.html", username=username)


def get_db_connection():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="test",
            database="project_db"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

    return connection


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
