import json
import os

import requests
from flask import Flask, flash, jsonify, make_response, redirect, render_template, request, url_for

from scraper import get_course_table, get_graduate_info, get_student_course, get_student_progress, run

app = Flask(__name__)
app.config['SECRET_KEY'] = '3c178af81e8f023e05fc72c56757417158aaeff46e23263df647d9fdc4ad2452'
app.config['JSON_AS_ASCII'] = False

# decode course data from course_data.json
course_data = json.load(open(os.path.join(app.root_path, 'course_data.json'), 'r', encoding='utf-8'))


@app.route('/')
def index():
    return render_template('terms_of_service.html')


@app.route('/home')
def home():
    cookie_account = request.cookies.get('Account')
    cookie_password = request.cookies.get('Password')
    cookie_name = request.cookies.get('Name')

    user_name = '訪客'
    user_id = '-'
    has_logged_in = 'False'

    if cookie_account is not None and cookie_password is not None:
        has_logged_in = 'True'
        user_name = cookie_name
        user_id = cookie_account
    return render_template('home.html',
                           userName=user_name,
                           userId=user_id,
                           hasLoggedIn=has_logged_in,
                           courseData=course_data)


@app.route('/profile')
def profile():
    cookie_account = request.cookies.get('Account')
    cookie_password = request.cookies.get('Password')
    cookie_name = request.cookies.get('Name')

    if cookie_account is None or cookie_password is None:
        return redirect(url_for('login'))

    user_name = cookie_name
    student_course_data = get_student_course(run(cookie_account, cookie_password))
    student_course_credits = get_student_progress(
        run(cookie_account, cookie_password))
    student_graduate_info = get_graduate_info(cookie_account, cookie_password)

    user_pic_url = '/static/img/user.png'
    # r = requests.get(
    #     'http://elearning.nuk.edu.tw/_uploadfiles/stuphoto/' + cookie_account.lower() + '.jpg')
    # if r.status_code == 200:
    #     user_pic_url = 'http://elearning.nuk.edu.tw/_uploadfiles/stuphoto/' + \
    #                    cookie_account.lower() + '.jpg'

    return render_template('profile.html',
                           userName=user_name,
                           userId=cookie_account,
                           userPicUrl=user_pic_url,
                           studentGraduateInfo=student_graduate_info,
                           studentCourseData=student_course_data,
                           studentCourseCredits=student_course_credits)


@app.route('/guide')
def guide():
    cookie_account = request.cookies.get('Account')
    cookie_password = request.cookies.get('Password')
    cookie_name = request.cookies.get('Name')

    user_name = '訪客'
    user_id = '-'
    has_logged_in = 'False'

    if cookie_account is not None and cookie_password is not None:
        has_logged_in = 'True'
        user_name = cookie_name
        user_id = cookie_account

    return render_template('how_to_use.html',
                           userName=user_name,
                           userId=user_id,
                           hasLoggedIn=has_logged_in)


@app.route('/login', methods=['GET', 'POST'])
def login():
    cookie_account = request.cookies.get('Account')
    cookie_password = request.cookies.get('Password')
    if cookie_account is not None and cookie_password is not None:
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

    if res.headers['Content-Length'] != '969':
        student_graduate_info = get_graduate_info(account, password)  # 取得學生基本資料
        view_response = make_response(redirect(url_for('profile')))
        view_response.set_cookie('Name', student_graduate_info['student_name'])
        view_response.set_cookie('Account', account)
        view_response.set_cookie('Password', password)
        return view_response
    flash('教務系統說登入錯誤', 'danger')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if request.cookies.get('Account') is not None:
        res = make_response(redirect(url_for('home')))
        res.delete_cookie('Account')
        res.delete_cookie('Password')
        res.delete_cookie('Name')
        return res
    return redirect(url_for('home'))


# ===== 手機頁面路由 ===== #

@app.route('/m/home')
def mobile_home():
    cookie_account = request.cookies.get('Account')
    cookie_password = request.cookies.get('Password')
    cookie_name = request.cookies.get('Name')

    user_name = '訪客'
    user_id = '-'
    has_logged_in = 'False'

    if cookie_account is not None and cookie_password is not None:
        has_logged_in = 'True'
        user_name = cookie_name
        user_id = cookie_account

    return render_template('mobile_home.html',
                           userName=user_name,
                           userId=user_id,
                           hasLoggedIn=has_logged_in,
                           courseData=course_data)


@app.route('/m/profile')
def mobile_profile():
    cookie_account = request.cookies.get('Account')
    cookie_password = request.cookies.get('Password')
    cookie_name = request.cookies.get('Name')

    if cookie_account is None or cookie_password is None:
        return redirect(url_for('mobile_login'))

    user_name = cookie_name
    student_course_data = get_student_course(run(cookie_account, cookie_password))
    student_course_credits = get_student_progress(
        run(cookie_account, cookie_password))
    student_graduate_info = get_graduate_info(cookie_account, cookie_password)

    user_pic_url = '/static/img/user.png'
    # r = requests.get(
    #     'http://elearning.nuk.edu.tw/_uploadfiles/stuphoto/' + cookie_account.lower() + '.jpg')
    # if r.status_code == 200:
    #     user_pic_url = 'http://elearning.nuk.edu.tw/_uploadfiles/stuphoto/' + \
    #                    cookie_account.lower() + '.jpg'

    return render_template('mobile_profile.html',
                           userName=user_name,
                           userId=cookie_account,
                           userPicUrl=user_pic_url,
                           studentGraduateInfo=student_graduate_info,
                           studentCourseData=student_course_data,
                           studentCourseCredits=student_course_credits)


@app.route('/m/login', methods=['GET', 'POST'])
def mobile_login():
    cookie_account = request.cookies.get('Account')
    cookie_password = request.cookies.get('Password')

    if cookie_account is not None and cookie_password is not None:
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

    if res.headers['Content-Length'] != '969':
        student_graduate_info = get_graduate_info(account, password)  # 取得學生基本資料
        view_response = make_response(redirect(url_for('mobile_profile')))
        view_response.set_cookie('Name', student_graduate_info['student_name'])
        view_response.set_cookie('Account', account)
        view_response.set_cookie('Password', password)
        return view_response
    flash('教務系統說登入錯誤', 'danger')
    return redirect(url_for('mobile_login'))


@app.route('/m/logout')
def mobile_logout():
    if request.cookies.get('Account') is not None:
        res = make_response(redirect(url_for('mobile_home')))
        res.delete_cookie('Account')
        res.delete_cookie('Password')
        res.delete_cookie('Name')
        return res
    return redirect(url_for('mobile_home'))


# ===== API ===== #

@app.route('/getInfo/<account>&<password>')
def get_info(account, password):
    return jsonify(get_graduate_info(account, password))


@app.route('/getCourse/<account>&<password>')
def get_course(account, password):
    return jsonify(get_student_course(run(account, password)))


@app.route('/getProgress/<account>&<password>')
def get_progress(account, password):
    return jsonify(get_student_progress(run(account, password)))


@app.route('/getTable/<account>&<password>')
def get_table(account, password):
    return jsonify(get_course_table(account, password))


if __name__ == "__main__":
    app.run()
