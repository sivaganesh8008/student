from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

# Allow React to connect to Flask
CORS(app)

DATABASE = "students.db"


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==================================================
# INITIALIZE DATABASE
# ==================================================

def init_db():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pin TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully!")


# ==================================================
# HOME
# ==================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Student Management API is running"
    })


# ==================================================
# ADD STUDENT
# POST /students
# ==================================================

@app.route("/students", methods=["POST"])
def add_student():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        name = data.get("name")
        pin = data.get("pin")

        # Check empty values
        if not name or not pin:

            return jsonify({
                "message": "Name and PIN are required"
            }), 400

        name = name.strip()
        pin = pin.strip()

        if not name or not pin:

            return jsonify({
                "message": "Name and PIN cannot be empty"
            }), 400

        conn = get_db_connection()

        cursor = conn.execute(
            """
            INSERT INTO students (name, pin)
            VALUES (?, ?)
            """,
            (name, pin)
        )

        conn.commit()

        student_id = cursor.lastrowid

        conn.close()

        return jsonify({
            "message": "Student added successfully",
            "student": {
                "id": student_id,
                "name": name,
                "pin": pin
            }
        }), 201

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "message": "Something went wrong",
            "error": str(e)
        }), 500


# ==================================================
# GET ALL STUDENTS
# GET /students
# ==================================================

@app.route("/students", methods=["GET"])
def get_all_students():

    try:

        conn = get_db_connection()

        students = conn.execute(
            """
            SELECT id, name, pin
            FROM students
            ORDER BY id ASC
            """
        ).fetchall()

        conn.close()

        result = []

        for student in students:

            result.append({
                "id": student["id"],
                "name": student["name"],
                "pin": student["pin"]
            })

        return jsonify(result), 200

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "message": "Unable to get students",
            "error": str(e)
        }), 500


# ==================================================
# GET ONE STUDENT
# GET /students/<id>
# ==================================================

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):

    try:

        conn = get_db_connection()

        student = conn.execute(
            """
            SELECT id, name, pin
            FROM students
            WHERE id = ?
            """,
            (student_id,)
        ).fetchone()

        conn.close()

        if student is None:

            return jsonify({
                "message": "Student not found"
            }), 404

        return jsonify({
            "id": student["id"],
            "name": student["name"],
            "pin": student["pin"]
        }), 200

    except Exception as e:

        return jsonify({
            "message": "Something went wrong",
            "error": str(e)
        }), 500


# ==================================================
# UPDATE STUDENT
# PUT /students/<id>
# ==================================================

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "message": "No data received"
            }), 400

        name = data.get("name")
        pin = data.get("pin")

        if not name or not pin:

            return jsonify({
                "message": "Name and PIN are required"
            }), 400

        name = name.strip()
        pin = pin.strip()

        conn = get_db_connection()

        # Check student
        student = conn.execute(
            """
            SELECT id
            FROM students
            WHERE id = ?
            """,
            (student_id,)
        ).fetchone()

        if student is None:

            conn.close()

            return jsonify({
                "message": "Student not found"
            }), 404

        # Update
        conn.execute(
            """
            UPDATE students
            SET name = ?, pin = ?
            WHERE id = ?
            """,
            (name, pin, student_id)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student updated successfully"
        }), 200

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "message": "Unable to update student",
            "error": str(e)
        }), 500


# ==================================================
# DELETE STUDENT
# DELETE /students/<id>
# ==================================================

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    try:

        conn = get_db_connection()

        student = conn.execute(
            """
            SELECT id
            FROM students
            WHERE id = ?
            """,
            (student_id,)
        ).fetchone()

        if student is None:

            conn.close()

            return jsonify({
                "message": "Student not found"
            }), 404

        conn.execute(
            """
            DELETE FROM students
            WHERE id = ?
            """,
            (student_id,)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student deleted successfully"
        }), 200

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "message": "Unable to delete student",
            "error": str(e)
        }), 500


# ==================================================
# START SERVER
# ==================================================

if __name__ == "__main__":

    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )