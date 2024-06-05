import os

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)

LOG_NAME = "flask-app-internal-logs"

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel('models/gemini-pro')


def response(message):
    resp = model.generate_content(message)
    return resp.text

@app.route('/')
def index():
    ###
    return render_template('index.html')


@app.route('/response', methods=['GET', 'POST'])
def get_response():
    user_input = ""
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    else:
        user_input = request.form['user_input']

    content = response(user_input)
    return jsonify(content=content)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
