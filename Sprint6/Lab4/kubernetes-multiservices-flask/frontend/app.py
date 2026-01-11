from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    try:
        response = requests.get('http://backend-service:5000/')
        data = response.json()
        message = data.get('message', 'No message received')
    except Exception as e:
        message = f"Error: {e}"
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)