from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

connection = mysql.connector.connect(
    host=os.environ.get("MYSQL_HOST", "mysql-service"),
    user=os.environ.get("MYSQL_USER", "user"),
    password=os.environ.get("MYSQL_PASSWORD", "password"),
    database=os.environ.get("MYSQL_DATABASE", "test_db"),
)


@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("SELECT text FROM message LIMIT 1;")
    result = cursor.fetchone()
    cursor.close()
    return jsonify({"message": result[0] if result else "No message found"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
