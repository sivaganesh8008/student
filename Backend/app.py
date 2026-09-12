from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = "students.db"


# Create database and table
def init_db():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pin TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Add student
@app.route("/students", methods=["POST"])
def add_student():

    data = request.json

    name = data.get("name")
    pin = data.get("pin")

    if not name or not pin:
        return jsonify({
            "message": "Name and PIN are required"
        }), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, pin) VALUES (?, ?)",
        (name, pin)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student added successfully"
    }), 201


# Get all students
@app.route("/students", methods=["GET"])
def get_students():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, pin FROM students")

    students = cursor.fetchall()

    conn.close()

    result = []

    for student in students:
        result.append({
            "id": student[0],
            "name": student[1],
            "pin": student[2]
        })

    return jsonify(result)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
