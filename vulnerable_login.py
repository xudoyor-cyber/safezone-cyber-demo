from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Подключение к базе и создание курсора
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы и добавление тестового пользователя
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
    conn.commit()

# HTML шаблон
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Login (Do Not Use in Real Life)</title>
</head>
<body>
    <h2>Vulnerable Login (Do Not Use in Real Life)</h2>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username"><br>
        <label>Password:</label>
        <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form>
    {% if error %}
        <p style="color:red;">❌ {{ error }}</p>
    {% elif success %}
        <p style="color:green;">✅ {{ success }}</p>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    success = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # УЯЗВИМЫЙ ЗАПРОС (SQL Injection возможен!)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("Executing:", query)
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            success = "You are logged in!"
        else:
            error = "Invalid credentials"

    return render_template_string(template, error=error, success=success)

if __name__ == "__main__":
    app.run(debug=True)

