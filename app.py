from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from scraper import run, get_student_course, get_student_progress
import requests
import json
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = '3c178af81e8f023e05fc72c56757417158aaeff46e23263df647d9fdc4ad2452'

ENV = 'PROD'

if ENV == 'DEV':
    with open('static\\json\\course.json', 'r', encoding='utf-8-sig') as jsonFile2:
        courseData = json.load(jsonFile2)
else:
    url = 'https://e7401c50-a59b-4ef9-9a40-a5ddf3852603.mock.pstmn.io/courseData'
    response = requests.get(url)
    courseData = json.loads(response.text)


@app.route('/')
def index():
    cookieAccount = request.cookies.get('Account')
    cookiePassword = request.cookies.get('Password')
    hasLoggedIn = 'False'
    if cookieAccount != None and cookiePassword != None:
        hasLoggedIn = 'True'
    return render_template('index.html', hasLoggedIn=hasLoggedIn, courseData=courseData)


@app.route('/login', methods=['GET', 'POST'])
def login():
    cookieAccount = request.cookies.get('Account')
    cookiePassword = request.cookies.get('Password')
    if cookieAccount != None and cookiePassword != None:
        return redirect(url_for('profile'))

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
        response = make_response(redirect(url_for('profile')))
        response.set_cookie('Account', account)
        response.set_cookie('Password', password)
        return response
    else:
        flash('教務系統說登入錯誤', 'danger')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if request.cookies.get('Account') != None:
        res = make_response(redirect(url_for('index')))
        res.delete_cookie('Account')
        res.delete_cookie('Password')
        return res
    else:
        return redirect(url_for('index'))


@app.route('/profile')
def profile():
    cookieAccount = request.cookies.get('Account')
    cookiePassword = request.cookies.get('Password')
    if cookieAccount == None or cookiePassword == None:
        return redirect(url_for('login'))

    studentCourseData = get_student_course(run(cookieAccount, cookiePassword))
    studentCourseCredits = get_student_progress(run(cookieAccount, cookiePassword))
    return render_template('profile.html',
                            studentCourseData=studentCourseData,
                            studentCourseCredits=studentCourseCredits)


if __name__ == "__main__":
    app.run(debug=True)
