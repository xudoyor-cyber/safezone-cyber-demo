
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize in-memory database for demo
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', '1234')")
    conn.commit()
    return conn

db_conn = init_db()

@app.route('/')
def home():
    return render_template_string("""
        <h2>Safe Login Demo (using prepared statements)</h2>
        <form action="/login" method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    """)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        return "✅ Login successful! Welcome."
    else:
        return "❌ Invalid credentials."

if __name__ == '__main__':
    app.run(debug=True)
