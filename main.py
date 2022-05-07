from flask import Flask, render_template, request
from datetime import date
import sqlite3

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def home():
    def clear_table():
        db_connection = sqlite3.connect("static/notes.db")
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM notes")
        db_connection.commit()
        cursor.execute("VACUUM")
        db_connection.commit()

    db_connection = sqlite3.connect("static/notes.db")
    cursor = db_connection.cursor()

    # Create table if not existent
    cursor.execute("CREATE TABLE IF NOT EXISTS notes (note_id INTEGER PRIMARY KEY, date DATE, title VARCHAR(30), text TEXT)")

    if request.method == "GET":
        current_date = date.today()

        data = cursor.execute("SELECT * FROM notes")
        rows = cursor.fetchall()
        notes = []

        for row in rows:
            notes.append(row)

        return render_template('index.html', date=current_date, notes=notes, clear_table=clear_table)

    if request.method == "POST":
        current_date = date.today()
        title = request.form.get('title')
        text = request.form.get('text')

        statement = "INSERT INTO notes (date, title, text) VALUES ({}, '{}', '{}')".format(current_date, title, text)
        cursor.execute(statement)
        db_connection.commit()

        return render_template('index.html')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="localhost", port="8080", debug=True)
    db_connection.close()
