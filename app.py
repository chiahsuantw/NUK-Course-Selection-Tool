from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

ENV = 'PROD'

if ENV == 'DEV':
    with open('static\\json\\course.json', 'r', encoding='utf-8-sig') as jsonFile:
        courseData = json.load(jsonFile)
else:
    url = 'https://e7401c50-a59b-4ef9-9a40-a5ddf3852603.mock.pstmn.io/courseData'
    response = requests.get(url)
    courseData = json.loads(response.text)


@app.route('/')
def index():
    return render_template('index.html', courseData=courseData)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile(user, pwd):
    return 'profile'

if __name__ == "__main__":
    app.run(debug=True)