from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# создаем БД и таблицу
def init_db():
    conn = sqlite3.connect('vulnerable_users.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("INSERT INTO users VALUES ('admin', '1234')")
    conn.commit()
    conn.close()

init_db()

# HTML-форма
login_form = '''
    <h2>Vulnerable Login (Do Not Use in Real Life)</h2>
    <form method="POST">
        Username: <input type="text" name="username" /><br/>
        Password: <input type="text" name="password" /><br/>
        <input type="submit" value="Login" />
    </form>
    <p>{{ message }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ❌ УЯЗВИМЫЙ SQL-запрос (НЕЛЬЗЯ ТАК ДЕЛАТЬ!)
        conn = sqlite3.connect('vulnerable_users.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing: {query}")  # для отладки
        c.execute(query)
        result = c.fetchone()
        conn.close()

        if result:
            message = '✅ Logged in successfully (INSECURE METHOD!)'
        else:
            message = '❌ Invalid credentials'

    return render_template_string(login_form, message=message)

if __name__ == '__main__':
    app.run(debug=True)
