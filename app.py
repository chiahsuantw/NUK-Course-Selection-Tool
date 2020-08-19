from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from scraper import run, get_student_course, get_student_progress, get_graduate_info
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
    return redirect(url_for('home'))


@app.route('/home')
def home():
    cookieAccount = request.cookies.get('Account')
    cookiePassword = request.cookies.get('Password')
    cookieName = request.cookies.get('Name')
    
    userName = '訪客'
    userId = 'A0000000'
    hasLoggedIn = 'False'
    
    if cookieAccount != None and cookiePassword != None:
        hasLoggedIn = 'True'
        userName = cookieName
        userId = cookieAccount
    return render_template('home.html', 
                            userName=userName, 
                            userId=userId, 
                            hasLoggedIn=hasLoggedIn, 
                            courseData=courseData)


@app.route('/profile')
def profile():
    cookieAccount = request.cookies.get('Account')
    cookiePassword = request.cookies.get('Password')
    cookieName = request.cookies.get('Name')

    if cookieAccount == None or cookiePassword == None:
        return redirect(url_for('login'))

    userName = cookieName
    studentCourseData = get_student_course(run(cookieAccount, cookiePassword))
    studentCourseCredits = get_student_progress(run(cookieAccount, cookiePassword))
    studentGraduateInfo = get_graduate_info(cookieAccount, cookiePassword)

    userPicUrl = '/static/img/user.png'
    r = requests.get('http://elearning.nuk.edu.tw/_uploadfiles/stuphoto/' + cookieAccount.lower() + '.jpg')
    if r.status_code == 200:
        userPicUrl = 'http://elearning.nuk.edu.tw/_uploadfiles/stuphoto/' + cookieAccount.lower() + '.jpg'
    
    return render_template('profile.html',
                            userName=userName,
                            userId=cookieAccount,
                            userPicUrl=userPicUrl,
                            studentGraduateInfo=studentGraduateInfo,
                            studentCourseData=studentCourseData,
                            studentCourseCredits=studentCourseCredits)


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
        studentGraduateInfo = get_graduate_info(account, password)  # 取得學生基本資料
        response = make_response(redirect(url_for('profile')))
        response.set_cookie('Name', studentGraduateInfo['student_name'])
        response.set_cookie('Account', account)
        response.set_cookie('Password', password)
        return response
    else:
        flash('教務系統說登入錯誤', 'danger')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if request.cookies.get('Account') != None:
        res = make_response(redirect(url_for('home')))
        res.delete_cookie('Account')
        res.delete_cookie('Password')
        res.delete_cookie('Name')
        return res
    else:
        return redirect(url_for('home'))


@app.route('/m/home')
def mobile_home():
    cookieAccount = request.cookies.get('Account')
    cookiePassword = request.cookies.get('Password')
    cookieName = request.cookies.get('Name')
    
    userName = '訪客'
    userId = 'A0000000'
    hasLoggedIn = 'False'
    
    if cookieAccount != None and cookiePassword != None:
        hasLoggedIn = 'True'
        userName = cookieName
        userId = cookieAccount
    return render_template('mobile_home.html', 
                            userName=userName, 
                            userId=userId, 
                            hasLoggedIn=hasLoggedIn, 
                            courseData=courseData)


@app.route('/m/profile')
def mobile_profile():
    cookieAccount = request.cookies.get('Account')
    cookiePassword = request.cookies.get('Password')
    cookieName = request.cookies.get('Name')

    if cookieAccount == None or cookiePassword == None:
        return redirect(url_for('login'))

    userName = cookieName
    studentCourseData = get_student_course(run(cookieAccount, cookiePassword))
    studentCourseCredits = get_student_progress(run(cookieAccount, cookiePassword))
    studentGraduateInfo = get_graduate_info(cookieAccount, cookiePassword)

    userPicUrl = '/static/img/user.png'
    r = requests.get('http://elearning.nuk.edu.tw/_uploadfiles/stuphoto/' + cookieAccount.lower() + '.jpg')
    if r.status_code == 200:
        userPicUrl = 'http://elearning.nuk.edu.tw/_uploadfiles/stuphoto/' + cookieAccount.lower() + '.jpg'
    
    return render_template('mobile_profile.html',
                            userName=userName,
                            userId=cookieAccount,
                            userPicUrl=userPicUrl,
                            studentGraduateInfo=studentGraduateInfo,
                            studentCourseData=studentCourseData,
                            studentCourseCredits=studentCourseCredits)


@app.route('/m/login', methods=['GET', 'POST'])
def mobile_login():
    cookieAccount = request.cookies.get('Account')
    cookiePassword = request.cookies.get('Password')
    if cookieAccount != None and cookiePassword != None:
        return redirect(url_for('mobile_profile'))

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
        studentGraduateInfo = get_graduate_info(account, password)  # 取得學生基本資料
        response = make_response(redirect(url_for('mobile_profile')))
        response.set_cookie('Name', studentGraduateInfo['student_name'])
        response.set_cookie('Account', account)
        response.set_cookie('Password', password)
        return response
    else:
        flash('教務系統說登入錯誤', 'danger')
        return redirect(url_for('mobile_login'))


@app.route('/m/logout')
def mobile_logout():
    if request.cookies.get('Account') != None:
        res = make_response(redirect(url_for('mobile_home')))
        res.delete_cookie('Account')
        res.delete_cookie('Password')
        res.delete_cookie('Name')
        return res
    else:
        return redirect(url_for('mobile_home'))

if __name__ == "__main__":
    app.run(debug=True)
