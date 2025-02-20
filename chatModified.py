import mysql.connector
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # Allow frontend to communicate with backend

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Swix@7466',
        database='yoga_project'
    )

@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()  # Convert input to lowercase
    response = "I didn't understand that. Please ask about a yoga pose or give feedback."

    # Connect to the database
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    # Fetch pose description from MySQL
    cursor.execute("SELECT poseDescription FROM pose WHERE LOWER(poseName) = %s", (user_message,))
    result = cursor.fetchone()

    if result:
        response = result["poseDescription"]

    # Close database connection
    cursor.close()
    con.close()

    return jsonify({"response": response})

@app.route("/feedback", methods=["POST"])
def feedback():
    user_feedback = request.json.get("feedback", "")
    user_id = request.json.get("userID", None)  # Get user ID (optional)
    pose_id = request.json.get("poseID", None)  # Get pose ID (optional)

    if user_feedback:
        con = get_db_connection()
        cursor = con.cursor()

        # Insert into feedback table with userID & poseID
        cursor.execute("INSERT INTO feedback (userID, poseID, feedback) VALUES (%s, %s, %s)", 
                       (user_id, pose_id, user_feedback))
        
        con.commit()
        cursor.close()
        con.close()
        return jsonify({"message": "Thank you for your feedback!"})

    return jsonify({"message": "Feedback cannot be empty."}), 400

@app.route("/get_feedback", methods=["GET"])
def get_feedback():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedback")
    feedback_data = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify({"feedback": feedback_data})

if __name__ == "__main__":
    app.run(debug=True)
