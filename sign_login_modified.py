from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# MySQL Configuration (Update credentials if needed)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change this if different
app.config['MYSQL_PASSWORD'] = 'Swix@7466'  # Set your actual MySQL password
app.config['MYSQL_DB'] = 'yoga_project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('LoginAndSignup.html')  # Ensure this file is in the 'templates' folder

# User Registration
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    useremail = request.form.get('email')
    password = request.form.get('password')

    if not username or not useremail or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, useremail, password) VALUES (%s, %s, %s)", 
                    (username, useremail, hashed_password))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
