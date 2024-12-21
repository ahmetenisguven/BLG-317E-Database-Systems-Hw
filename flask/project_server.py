from flask import Flask, render_template, request, redirect, url_for, flash
import mysql
from mysql.connector import Error
from operator import itemgetter
from types import NoneType
import random
from flask import session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.context_processor
def inject_tables():
    """Injects all table names into the context for the layout."""
    connection = get_db_connection()  # Get a database connection
    tables = []  # Default empty list for table names
    mapped_table_name = [ ]

    if connection:  # If the connection is successful
        try:
            cursor = connection.cursor()  # Create a cursor
            cursor.execute("SHOW TABLES;")  # Query to get all table names
            # Convert rows to table names
            tables = [row[0] for row in cursor.fetchall()]  # Modify the index to 0 for table names
            cursor.close()  # Close the cursor manually

            mapped_table_name = [table_name_mapping.get(table, table.replace('_', ' ').title()) for table in tables]
        except Exception as e:
            print(f"Error fetching tables: {e}")  # Log error if query fails
        finally:
            connection.close()  # Close the database connection

    return {'tables': tables, 'mapped_tables': mapped_table_name}  # This will inject 'tables' into every template


@app.route('/login', methods=('GET', 'POST'))
def home_page():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'password2' in request.form:
            user_name = request.form['username']
            password = request.form['password']
            password2 = request.form['password2']

            if not user_name or not password or not password2:
                flash("There cannot be empty values.", "warning")
                return render_template("index.html")

            if password != password2:
                flash("Two passwords must be same.", "warning")
                return render_template("index.html")

            connection = get_db_connection()

            if connection is None:
                flash("Connection Failed.", "danger")
                return render_template("index.html")
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("INSERT INTO users(user_name, user_password) VALUES(%s,%s)", (user_name, password))
                connection.commit()
                flash("Registered Successfully.", "success")
                app.secret_key = user_name 
                return game_page(user_name)
            except Error:
                flash(f"Same Username exists!", "danger")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        elif 'username_delete' in request.form and 'password_delete' in request.form:
            user_name = request.form['username_delete']
            password = request.form['password_delete']

            connection = get_db_connection()
            if connection is None:
                flash("Connection Failed.", "danger")
                return render_template("index.html")

            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_name=%s;", (user_name,))
            the_user = cursor.fetchone()

            if type(the_user) is NoneType:
                flash("Username does not exist.", "warning")
                cursor.close()
                connection.close()
                return render_template("index.html")

            if the_user.get('user_password') != password:
                flash("Wrong Password.", "warning")
                cursor.close()
                connection.close()
                return render_template("index.html")

            cursor.execute("DELETE FROM users WHERE user_name=%s", (user_name,))
            connection.commit()
            flash("Deleted Successfully.", "success")
            session.clear()
            cursor.close()
            connection.close()

            return render_template("index.html")

        elif 'username_login' in request.form and 'password_login' in request.form:
            user_name = request.form['username_login']
            password = request.form['password_login']

            if not user_name or not password:
                flash("There cannot be empty values.", "warning")
                return render_template("index.html")

            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_name=%s;", (user_name,))
            the_user = cursor.fetchone()

            if type(the_user) is NoneType:
                flash("Username does not exist.", "warning")
                cursor.close()
                connection.close()
                return render_template("index.html")

            if the_user.get('user_password') != password:
                flash("Wrong Password.", "warning")
                cursor.close()
                connection.close()
                return render_template("index.html")
            cursor.close()
            connection.close()

            app.secret_key = user_name 

            return game_page(user_name)

    return render_template("index.html")

column_mapping = {
    'code' : 'Code',
    'current_status': 'Current Status',
    'name': 'Name',
    'name_short': 'Name Shorted',
    'name_tv': 'Name on TV',
    'gender': 'Gender',
    'job_title': 'Job',
    'country_code' : 'Country Code',	
    'height_' : 'Height', 	
    'weight_' : 'Weight',	
    'sport'   : 'Sport',	
    'events'  : 'Events Participated',	
    'birth_date' : 'Birth Date',	
    'lang': 'Languages Spoken',
    'country': 'Country',
    'country_long': 'Official Country Name',
    'medal_date' :'Medal Earned Date',	
    'medal_type' : 'Type of Medal ' ,	
    'athletes_code' : 'Team of the Athlete', 	
    'teams_code' : 'Code of the Team',
    'sport_code' : 'Code of the Sport',
    'sport_URL' : 'URL for more info',
    'team' : 'Team',
    'team_gender' : 'Gender',	
    'country_code' : 'Country Code',
    'num_athletes' : 'Number of Athletes', 
    'num_coaches' : 'Number of Coaches',
    'roles' : 'Assigned Role',
    'coaches_code' : 'Code of the Coach',
    'user_name' : 'Username',       	
    'high_score' : 'Score', 	
    'game_played' : 'Games Played',
    'register_date' : 'Date of Registeration'
}

table_name_mapping = {
    'athletes' : 'Athletes',
    'coaches' : 'Coaches',
    'countries' : 'Countries',
    'medals' : 'Medals',
    'sport' : 'Sports',
    'teams': 'Teams',
    'teams_member' : 'Teams & Members',
    'users' : 'ScoreBoard'
}


@app.route('/tables')
def tables_page():
    connection = get_db_connection()
    if connection is None:
        flash("Couldn't connect to the database!", "danger")
        return render_template("tables.html", tables=[])

    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
    except Error as e:
        flash(f"Query failed: {e}", "danger")
        tables = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return render_template("tables.html", tables=tables)

@app.route('/tables/<table_name>')
def table_page(table_name):
    connection = get_db_connection()

    mapped_table_name = table_name_mapping.get(table_name, table_name.replace('_', ' ').title())

    if connection is None:
        flash("Couldn't connect to the database!", "danger")
        return render_template("table.html", table_name=table_name, columns=[], rows=[])

    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for better readability
        cursor.execute(f"DESCRIBE {table_name}")  # Get column names
        columns = [column['Field'] for column in cursor.fetchall()]  # Get column names from the result

        mapped_columns = [column_mapping.get(col, col.replace('_', ' ').title()) for col in columns]
        
        cursor.execute(f"SELECT * FROM {table_name}")  # Get all rows from the table
        rows = cursor.fetchall()  # Fetch all rows
        
    except Error as e:
        flash(f"Query failed: {e}", "danger")
        columns = []
        rows = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return render_template("table.html", table_name=mapped_table_name, columns=columns, mapped_columns=mapped_columns, rows=rows)


@app.route('/', methods=('GET', 'POST'))
def game_page(username="Guest", selected_athlete="NotSelected"):
    
    if username != "Guest":
        session['guesses_list'] = []
        session['selected_athlete'] = None
        session['user_name'] = username
        session['game_over'] = False

    if 'user_name' in session:
        username = session['user_name']


    connection = get_db_connection()
    if connection is None:
        flash("Couldn't connect to the database!", "danger")
        return render_template("game.html", username=username)

    cursor = connection.cursor(dictionary=True)

    if 'selected_athlete' not in session or session['selected_athlete'] is None:
        cursor.execute("select count(code) from athletes")
        athlete_count = cursor.fetchone()
        athlete_count = athlete_count.get('count(code)')

        select_random = random.randint(0, athlete_count - 1)

        cursor.execute("SELECT a.name AS athlete_name, a.gender, c.country_long, s.sport, TIMESTAMPDIFF(YEAR, a.birth_date, CURDATE()) AS age, IFNULL(GROUP_CONCAT(DISTINCT CONCAT(t.team, ' ', s.sport, ' ', IFNULL(t.events, ''), ' Team') SEPARATOR ', '),'No Team') AS teams_name, IFNULL(GROUP_CONCAT(m.medal_type SEPARATOR ', '),'No Medals') AS medals FROM athletes a LEFT JOIN countries c ON a.country_code = c.country_code LEFT JOIN sports s ON a.sport = s.sport LEFT JOIN teams_member tm ON a.code = tm.athletes_code LEFT JOIN teams t ON tm.teams_code = t.code LEFT JOIN medals m ON a.code = m.athletes_code GROUP BY a.name, a.gender, c.country_long, a.birth_date, s.sport LIMIT %s, 1", (select_random,))
        selected_athlete = cursor.fetchone()
        session['selected_athlete'] = selected_athlete
    else:
        selected_athlete = session['selected_athlete']
    

    name = selected_athlete.get('athlete_name')
    gender = selected_athlete.get('gender')
    country = selected_athlete.get('country_long')
    discipline = selected_athlete.get('sport')
    age = int(selected_athlete.get('age'))
    teams = sorted(parse_string(selected_athlete.get('teams_name')))
    medals = sorted(parse_string(selected_athlete.get('medals')))


    print(name, gender, country, discipline, age, teams, medals)

    cursor.execute("SELECT name FROM athletes ORDER BY name")
    athletes_dict = cursor.fetchall()
    athletes_list = [athletes_dict[i].get('name') for i in range(len(athletes_dict))]

    if 'guesses_list' not in session:
        session['guesses_list'] = []
    
    if request.method == 'POST':
        if 'log_out' in request.form:
            session.clear()
            session['guesses_list'] = []
            session['selected_athlete'] = None
            session['user_name'] = "Guest"
            session['game_over'] = False
            return home_page()

        elif 'reseter' in request.form:
            session.clear()
            session['guesses_list'] = []
            session['selected_athlete'] = None
            session['user_name'] = username
            session['game_over'] = False
            return render_template("game.html", username=username, athletes_list=athletes_list, guesses_list=session['guesses_list'])

        elif 'athlete_name' in request.form:
            user_selected_athlete_name = request.form['athlete_name']

            if session.get('game_over'):
                flash("The game is over! Reset to play again.", "warning")
            else:

                if user_selected_athlete_name not in athletes_list:
                    flash("This athlete does not exists in the database!", "warning")
                else:    
                    if any(user_selected_athlete_name in d.values() for d in session['guesses_list']):
                        flash("You've already guessed this athlete!", "warning")
                    else:
                        cursor.execute("SELECT a.name AS athlete_name, a.gender, c.country_long, s.sport, TIMESTAMPDIFF(YEAR, a.birth_date, CURDATE()) AS age, IFNULL(GROUP_CONCAT(DISTINCT CONCAT(t.team, ' ', s.sport, ' ', IFNULL(t.events, ''), ' Team') SEPARATOR ', '),'No Team') AS teams_name, IFNULL(GROUP_CONCAT(m.medal_type SEPARATOR ', '),'No Medals') AS medals FROM athletes a LEFT JOIN countries c ON a.country_code = c.country_code LEFT JOIN sports s ON a.sport = s.sport LEFT JOIN teams_member tm ON a.code = tm.athletes_code LEFT JOIN teams t ON tm.teams_code = t.code LEFT JOIN medals m ON a.code = m.athletes_code WHERE a.name = %s GROUP BY a.name, a.gender, c.country_long, a.birth_date, s.sport", (user_selected_athlete_name,))
                        user_selected_athlete_dict = cursor.fetchone()

                        session['green_count'] = 0

                        if user_selected_athlete_dict['athlete_name'] == name:
                            user_selected_athlete_dict['athlete_name_color'] = "green"
                            session['green_count'] += 1
                        elif any(item in sorted(user_selected_athlete_dict['athlete_name'].split()) for item in sorted(name.split())):
                            user_selected_athlete_dict['athlete_name_color'] = "yellow"
                        else:
                            user_selected_athlete_dict['athlete_name_color'] = "gray"

                        if user_selected_athlete_dict['gender'] == gender:
                            user_selected_athlete_dict['gender_color'] = "green"
                            session['green_count'] += 1
                        else:
                            user_selected_athlete_dict['gender_color'] = "gray"

                        if user_selected_athlete_dict['country_long'] == country:
                            user_selected_athlete_dict['country_long_color'] = "green"
                            session['green_count'] += 1
                        else:
                            user_selected_athlete_dict['country_long_color'] = "gray"

                        if user_selected_athlete_dict['sport'] == discipline:
                            user_selected_athlete_dict['sport_color'] = "green"
                            session['green_count'] += 1
                        else:
                            user_selected_athlete_dict['sport_color'] = "gray"

                        if user_selected_athlete_dict['age'] == age:
                            user_selected_athlete_dict['age_color'] = "green"
                            session['green_count'] += 1
                        elif abs(user_selected_athlete_dict['age'] - age) < 4:
                            user_selected_athlete_dict['age_color'] = "yellow"
                        else:
                            user_selected_athlete_dict['age_color'] = "gray"

                        if sorted(parse_string(user_selected_athlete_dict['teams_name'])) == teams:
                            user_selected_athlete_dict['teams_name_color'] = "green"
                            session['green_count'] += 1
                        elif any(item in sorted(parse_string(user_selected_athlete_dict['teams_name'])) for item in teams):
                            user_selected_athlete_dict['teams_name_color'] = "yellow"
                        else:
                            user_selected_athlete_dict['teams_name_color'] = "gray"

                        if sorted(parse_string(user_selected_athlete_dict['medals'])) == medals:
                            user_selected_athlete_dict['medals_color'] = "green"
                            session['green_count'] += 1
                        elif any(item in sorted(parse_string(user_selected_athlete_dict['medals'])) for item in medals):
                            user_selected_athlete_dict['medals_color'] = "yellow"
                        else:
                            user_selected_athlete_dict['medals_color'] = "gray"

                        session['guesses_list'].append(user_selected_athlete_dict)
                        session.modified = True

                        if session['green_count'] == 7:
                            flash("Congratulations! You won the game!", "success")
                            session['game_over'] = True

                            if username != "Guest":
                                cursor.execute("UPDATE users SET game_played = game_played+1 WHERE user_name = %s", (session['user_name'],))
                                connection.commit()

                                cursor.execute("SELECT high_score FROM users WHERE user_name = %s", (session['user_name'],))
                                get_prev_high_score = cursor.fetchone()

                                if get_prev_high_score['high_score'] > len(session['guesses_list']):
                                    cursor.execute("UPDATE users SET high_score = %s WHERE user_name = %s", (len(session['guesses_list']), session['user_name']))
                                    connection.commit()
                
                    
            cursor.close()
            connection.close()
            return render_template("game.html", username=username, athletes_list=athletes_list, guesses_list=session['guesses_list'])

    cursor.close()
    connection.close()
    return render_template("game.html", username=username, athletes_list=athletes_list, guesses_list=session['guesses_list'])


def parse_string(input_string):
    if "," in input_string:
        return input_string.split(",")
    return [input_string]


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # needs to be changed in different database storage methods
            user="root",  # needs to be changed in different database storage methods
            password="test",  # needs to be changed in different computers
            database="project_db"  # needs to be changed in different computers
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

    return connection


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)