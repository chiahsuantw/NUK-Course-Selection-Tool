from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '3c178af81e8f023e05fc72c56757417158aaeff46e23263df647d9fdc4ad2452'

ENV = 'PROD'

with open('static\\json\\studentCourse.json', 'r', encoding='utf-8-sig') as jsonFile1:
    studentCourseData = json.load(jsonFile1)

with open('static\\json\\student_credits.json', 'r', encoding='utf-8-sig') as jsonFile3:
    studentCourseCredits = json.load(jsonFile3)

if ENV == 'DEV':
    with open('static\\json\\course.json', 'r', encoding='utf-8-sig') as jsonFile2:
        courseData = json.load(jsonFile2)
else:
    url = 'https://e7401c50-a59b-4ef9-9a40-a5ddf3852603.mock.pstmn.io/courseData'
    response = requests.get(url)
    courseData = json.loads(response.text)


@app.route('/')
def index():
    return render_template('index.html', courseData=courseData)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    account = request.form['account']
    password = request.form['password']

    res = requests.post(
        'https://aca.nuk.edu.tw/Student2/Menu1.asp',
        {
            'Account': account,
            'Password': password
        })
    res.encoding = 'big5'

    if res.headers['Content-Length'] != '992':
        return redirect(url_for('profile'))
    else:
        flash('教務系統說登入錯誤', 'danger')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    return 'logout'


@app.route('/profile')
def profile():
    return render_template('profile.html', studentCourseData=studentCourseData, studentCourseCredits=studentCourseCredits)


if __name__ == "__main__":
    app.run(debug=True)
