import re

import bs4
import pandas as pd
import requests

# ==================== #
# 系所代碼
# ==================== #

course_code = {'通識微學分': 'MI',
               '共同必修系列': 'GR',
               '核心通識': 'CC',
               '通識人文科學類': 'LI',
               '通識自然科學類': 'SC',
               '通識社會科學類': 'SO',
               '全民國防教育類': 'CD',
               '興趣選修': 'IN',
               '西洋語文學系': 'WL',
               '運動健康與休閒學系': 'KH',
               '工藝與創意設計學系': 'CCD',
               '建築學系': 'DA',
               '創意設計與建築學系': 'CDA',
               '東亞語文學系': 'EL',
               '運動競技學系': 'DAP',
               '人文社會科學院共同課程': 'CHS',
               '法律學系': 'LA',
               '政治法律學系': 'GL',
               '財經法律學系': 'FL',
               '法學院共同課程': 'CCL',
               '應用經濟學系': 'AE',
               '金融管理學系': 'FI',
               '資訊管理學系': 'IM',
               '管理學院共同課程': 'CCM',
               '應用數學系': 'AM',
               '應用化學系': 'AC',
               '應用物理學系': 'AP',
               '理學院共同課程': 'CCS',
               '電機工程學系': 'EE',
               '土木與環境工程學系': 'CE',
               '資訊工程學系': 'CS',
               '化學工程及材料工程學系': 'CM',
               '生命科學系': 'LS',
               '亞太工商管理學系': 'AB',
               '國際學生系': 'ISP',
               '創新學院不分系': 'IFD'}


# ==================== #
# 爬修過的課
# ==================== #

def run(account, password):
    done_course = []
    req = requests.Session()
    req.post('https://aca.nuk.edu.tw/Student2/Menu1.asp',
             {'Account': account, 'Password': password})
    # Classno is your student ID
    # 爬修過的課
    r = req.post('https://aca.nuk.edu.tw/Student2/SO/ScoreQuery.asp',
                 data={'Classno': ''})
    r.encoding = 'big5'
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    soup = soup.select('table[border="1"] tr[align="center"] td')
    for i in range(int(len(soup) / 7)):
        compulsory = (soup[i * 7 + 3].text == "必修")
        done_course.append([soup[i * 7].text, soup[i * 7 + 1].text,
                            soup[i * 7 + 2].text, soup[i * 7 + 5].text, compulsory])

    r = req.get('https://aca.nuk.edu.tw/Graduate/GraduateDetail/Menu.asp')
    r.encoding = 'big5'
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    student = soup.find_all('center')[1].find('tr').text.split('　　　　　　')# 在畢業業條件多了一行，這裡是辨識學號及名字
    student_aca = student[2][3:]
    student_aca_code = course_code[student_aca]

    df_done_course = pd.DataFrame(
        done_course, columns=['id', 'name', 'credit', 'score', 'category'])

    for course in done_course:
        course_id = course[0]
        if course_id[0:4] == 'CCI1':
            df_done_course.loc[done_course.index(course), 'category'] = 'B1'
        elif course_id[0:4] == 'CCI2':
            df_done_course.loc[done_course.index(course), 'category'] = 'B2'
        elif course_id[0:4] == 'CCO3':
            df_done_course.loc[done_course.index(course), 'category'] = 'B3'
        elif course_id[0:4] == 'CCO4':
            df_done_course.loc[done_course.index(course), 'category'] = 'B4'
        elif course_id[0:4] == 'CCC5':
            df_done_course.loc[done_course.index(course), 'category'] = 'B5'
        elif course_id[0:4] == 'CCC6':
            df_done_course.loc[done_course.index(course), 'category'] = 'B6'
        elif course_id[0:2] == 'GR':
            if course_id[2:].isnumeric():
                df_done_course.loc[done_course.index(course), 'category'] = 'AC'
            elif course_id[-2].isalpha():
                df_done_course.loc[done_course.index(course), 'category'] = 'AE'
            else:
                df_done_course.loc[done_course.index(course), 'category'] = 'A3'
        elif course_id[0:2] == 'LI':
            df_done_course.loc[done_course.index(course), 'category'] = 'C1'
        elif course_id[0:2] == 'SO':
            df_done_course.loc[done_course.index(course), 'category'] = 'C2'
        elif course_id[0:2] == 'SC':
            df_done_course.loc[done_course.index(course), 'category'] = 'C3'
        else:
            if course_id[:len(student_aca_code)] != student_aca_code:
                # 跨院選修及微學分通識 'CD', 'IN', 'CHS', 'CCL', 'CCM', 'CCS'
                if course_id[:2] == 'CD' or course_id[:2] == 'IN':
                    df_done_course.loc[done_course.index(course), 'category'] = 'D1'
                elif course_id[:3] == 'CHS' or course_id[:3] == 'CCL' or course_id[:3] == 'CCM' or course_id[
                                                                                                   :3] == 'CCS':
                    df_done_course.loc[done_course.index(course), 'category'] = 'D1'
                else:
                    df_done_course.loc[done_course.index(course), 'category'] = 'D0'
            elif course[4]:
                df_done_course.loc[done_course.index(course), 'category'] = 'A1'
            else:
                df_done_course.loc[done_course.index(course), 'category'] = 'A2'
    return df_done_course


def get_graduate_info(account, password):
    req = requests.Session()
    req.post('https://aca.nuk.edu.tw/Student2/Menu1.asp',
             {'Account': account, 'Password': password})
    # 使用者資料(名字，學年，院所，院所代碼...)
    r = req.get('https://aca.nuk.edu.tw/Graduate/GraduateDetail/Menu.asp')
    r.encoding = 'big5'
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    student = soup.find_all('center')[1].find('tr').text.split('　　　　　　')
    student_name = student[1][3:]
    student_aca = student[2][3:]
    student_acayear = student[3][6:]
    student_aca_code = course_code[student_aca]

    # 畢業門檻調查
    r = req.post('https://aca.nuk.edu.tw/Graduate/GraduateData/QueryData.asp',
                 data={'Classno': account.upper(), 'Pclass': 'A', 'Sclass': student_aca_code.lower(), 'Gclass': 999,
                       'Yclass': account.upper(), 'Year': int(account[1:4])})
    r.encoding = 'big5'
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    graduate_condition = soup.find_all('td')[4:18]

    student_graduate_info = {'student_name': student_name,
                             'student_aca': student_aca,
                             'student_acayear': student_acayear,
                             'student_aca_code': student_aca_code}

    for i in range(0, 14, 2):
        student_graduate_info[graduate_condition[i].text.replace(
            '\u3000', '')] = graduate_condition[i + 1].text
    return student_graduate_info


def get_student_course(df_done_course):
    all_done_course = []  # 總課表

    # 將各 series 轉為 dict 放置 all_course list
    for i in range(len(df_done_course)):
        temp_course = df_done_course.loc[i,].to_dict()
        all_done_course.append(temp_course)

    return all_done_course


def get_student_progress(df_done_course):
    df_done_course.loc[df_done_course['score'] == '棄選', 'score'] = -70
    df_done_course.loc[df_done_course['score'] == '未送', 'score'] = -60
    df_done_course.loc[:, 'credit'] = df_done_course['credit'].astype('float')
    df_done_course.loc[:, 'score'] = df_done_course['score'].astype('float')

    df_done_course.loc[df_done_course['score'] < 60, 'credit'] = 0

    # Group by 'category'
    df_course_bar = df_done_course.groupby('category').sum().credit.to_dict()

    # 處理漏掉的項度
    cateclass = ['A1', 'A2', 'A3', 'AC', 'AE', 'B1',
                 'B2', 'B3', 'B4', 'B5', 'B6', 'C1', 'C2', 'C3', 'D0', 'D1']
    for cate in [cates for cates in cateclass if cates not in df_course_bar.keys()]:
        df_course_bar[cate] = 0.0

    return df_course_bar


def get_course_table(account, password):
    req = requests.Session()  # Session 儲存傳給伺服器的(對話)cookies

    req.post('https://course.nuk.edu.tw/Sel/SelectMain1.asp', {'Account': account, 'Password': password})
    r = req.get('https://course.nuk.edu.tw/Sel/query3.asp')
    r.encoding = 'big5'

    try:
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        tr_list = soup.find('table').find_all('tr')
    except:
        tr_list = []
        print(">>帳後密碼錯誤<<")

    course_list = []

    for tr in tr_list[1:]:
        c_d = {}
        raw_list = tr.text.split(' ')

        c_d['name'] = raw_list[3]
        c_d['credit'] = int(raw_list[5])
        c_d['time'] = time_split(raw_list[6])
        c_d['location'] = list(set(raw_list[7].split(',')))
        c_d['teacher'] = raw_list[8]

        course_list.append(c_d)

    return course_list


def time_split(raw_time):
    weekdays = '一二三四五六日'
    times = []
    period_list = []
    week_list = []

    for d in re.split(r'[^0-9X-Y]', raw_time):
        if d != '':
            period_list.append(d)
    for w in re.split(r'[0-9X-Y]', raw_time):
        if w != '':
            week_list.append(w)

    diff_week = list(set(week_list))

    for dd in diff_week:
        periods = []
        for i in range(len(week_list)):
            if week_list[i] == dd:
                periods.append(period_list[i])

        times.append([weekdays.find(dd) + 1, periods])
    return times
