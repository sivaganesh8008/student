from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

# Allow React frontend to communicate with Flask
CORS(app)

# SQLite database file
DATABASE = "students.db"


# --------------------------------------------------
# Database connection
# --------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)

    # Return database rows like dictionaries
    conn.row_factory = sqlite3.Row

    return conn


# --------------------------------------------------
# Create database and students table
# --------------------------------------------------
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


# --------------------------------------------------
# Home route
# --------------------------------------------------
@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Student API is running"
    })


# --------------------------------------------------
# Add student
# POST /students
# --------------------------------------------------
@app.route("/students", methods=["POST"])
def add_student():

    try:

        # Get JSON data from React
        data = request.get_json()

        # Check if data was received
        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        # Get name and PIN
        name = data.get("name")
        pin = data.get("pin")

        # Validate data
        if not name or not pin:

            return jsonify({
                "message": "Name and PIN are required"
            }), 400

        # Remove unnecessary spaces
        name = name.strip()
        pin = pin.strip()

        # Validate again after removing spaces
        if not name or not pin:

            return jsonify({
                "message": "Name and PIN cannot be empty"
            }), 400

        # Connect to database
        conn = get_db_connection()

        # Insert student
        cursor = conn.execute(
            """
            INSERT INTO students (name, pin)
            VALUES (?, ?)
            """,
            (name, pin)
        )

        # Save changes
        conn.commit()

        # Get newly created student ID
        student_id = cursor.lastrowid

        # Close connection
        conn.close()

        # Send response to React
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


# --------------------------------------------------
# Get all students
# GET /students
# --------------------------------------------------
@app.route("/students", methods=["GET"])
def get_students():

    try:

        # Connect to database
        conn = get_db_connection()

        # Get all students
        students = conn.execute(
            """
            SELECT id, name, pin
            FROM students
            ORDER BY id ASC
            """
        ).fetchall()

        # Close database
        conn.close()

        # Convert rows to dictionaries
        result = []

        for student in students:

            result.append({
                "id": student["id"],
                "name": student["name"],
                "pin": student["pin"]
            })

        # Return JSON
        return jsonify(result), 200

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "message": "Unable to get students",
            "error": str(e)
        }), 500


# --------------------------------------------------
# Get one student
# GET /students/<id>
# --------------------------------------------------
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

        # Student not found
        if student is None:

            return jsonify({
                "message": "Student not found"
            }), 404

        # Return student
        return jsonify({
            "id": student["id"],
            "name": student["name"],
            "pin": student["pin"]
        }), 200

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "message": "Something went wrong",
            "error": str(e)
        }), 500


# --------------------------------------------------
# Delete student
# DELETE /students/<id>
# --------------------------------------------------
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    try:

        conn = get_db_connection()

        # Check whether student exists
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

        # Delete student
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


# --------------------------------------------------
# Update student
# PUT /students/<id>
# --------------------------------------------------
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

        # Check if student exists
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

        # Update student
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
            "message": "Student updated successfully",
            "student": {
                "id": student_id,
                "name": name,
                "pin": pin
            }
        }), 200

    except Exception as e:

        print("Error:", e)

        return jsonify({
            "message": "Unable to update student",
            "error": str(e)
        }), 500


# --------------------------------------------------
# Start Flask server
# --------------------------------------------------
if __name__ == "__main__":

    # Create database/table
    init_db()

    # Start server
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

