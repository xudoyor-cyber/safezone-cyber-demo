from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("users_secure.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
    conn.commit()

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Login</title>
</head>
<body>
    <h2>Login Page (Secure)</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% elif success %}
        <p style="color: green;">{{ success }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    success = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()

            if result:
                success = "You are securely logged in!"
            else:
                error = "Invalid credentials"
        except Exception as e:
            error = f"Database error: {e}"

    return render_template_string(template, error=error, success=success)

if __name__ == "__main__":
    app.run(debug=True)
