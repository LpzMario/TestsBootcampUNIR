from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

connection = mysql.connector.connect(
    host=os.environ.get("DB_HOST", "db"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", "example"),
    database=os.environ.get("DB_NAME", "test_db"),
)


@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM greetings")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)


if __name__ == "__main__":
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS greetings (id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255));"
    )
    cursor.close()

if __name__ == "__main__":
    cursor = connection.cursor()
    cursor.execute("INSERT INTO greetings (message) VALUES ('Hello, world!');")
    cursor.close()
    app.run(host="0.0.0.0", debug=True)
