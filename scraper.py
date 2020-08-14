import bs4
import requests
import json
import pandas as pd

doneCourse = []
req = requests.Session()  # Seesion 儲存傳給伺服器的(對話)cookies
# if you wanna test this code, please input your account and password

account = ''
password = ''

def set_user_data(act, pwd):
    global account, password
    account = act
    password = pwd


print(account)
print(password)
# ==================== #
# 帳號密碼
account = 'a1085508'
password = 's125367799'
# ==================== #


req.post('https://aca.nuk.edu.tw/Student2/Menu1.asp',{'Account':account,'Password':password})
# Classno is your student ID


# ==================== # 
# 爬修過的課
# ==================== #
r = req.post('https://aca.nuk.edu.tw/Student2/SO/ScoreQuery.asp',data={'Classno':''})
r.encoding = 'big5'
soup = bs4.BeautifulSoup(r.text,'html.parser')
soup = soup.select('table[border="1"] tr[align="center"] td')
for i in range(int(len(soup)/7)):
    compulsory = (soup[i*7+3].text == "必修")
    doneCourse.append([soup[i*7].text,soup[i*7+1].text,soup[i*7+2].text,soup[i*7+5].text,compulsory])


# ==================== # 
# 系所代碼處理
# ==================== #
course_code = {'通識微學分': 'MI',
               '共同必修系列': 'GR',
               '核心通識': 'CC',
               '通識人文科學類': 'LI',
               '通識自然科學類': 'SC',
               '通識社會科學類': 'SO',
               '全民國防教育類': 'CD',
               '興趣選修': 'IN',
               '西洋語文學系': 'wl',
               '運動健康與休閒學系': 'kh',
               '工藝與創意設計學系': 'CCD',
               '建築學系': 'DA',
               '創意設計與建築學系': 'CDA',
               '東亞語文學系': 'EL',
               '運動競技學系': 'DAP',
               '人文社會科學院共同課程': 'CHS',
               '法律學系': 'la',
               '政治法律學系': 'GL',
               '財經法律學系': 'fl',
               '法學院共同課程': 'CCL',
               '應用經濟學系': 'ae',
               '金融管理學系': 'FI',
               '資訊管理學系': 'IM',
               '管理學院共同課程': 'CCM',
               '應用數學系': 'am',
               '應用化學系': 'ac',
               '應用物理學系': 'AP',
               '理學院共同課程': 'CCS',
               '電機工程學系': 'ee',
               '土木與環境工程學系': 'CE',
               '資訊工程學系': 'CS',
               '化學工程及材料工程學系': 'CM',
               '生命科學系': 'ls',
               '亞太工商管理學系': 'ab',
               '國際學生系': 'ISP',
               '創新學院不分系': 'IFD'}


# ==================== # 
# 取得學生年度、系所、系所代碼
# ==================== #
soup = bs4.BeautifulSoup(r.text,'html.parser')
student_name = soup.find_all('td')[3].text[3:]
student_aca = soup.find_all('td')[1].text[3:]
student_acayear = int(account[1:4])
student_aca_code = course_code[student_aca]

r = req.post('https://aca.nuk.edu.tw/Graduate/GraduateData/QueryData.asp',
            data={'Classno': account.upper(), 'Pclass': account[0].upper(), 'Sclass': student_aca_code.lower(), 'Gclass': 999, 'Yclass': account.upper(), 'Year': int(account[1:4])})
r.encoding = 'big5'
soup = bs4.BeautifulSoup(r.text,'html.parser')
graduate_condition = soup.find_all('td')[4:18]

student_graduate_info = {}
for i in range(0, 14, 2):
    student_graduate_info[graduate_condition[i].text.replace('\u3000', '')] = graduate_condition[i+1].text

df_doneCourse = pd.DataFrame(doneCourse, columns=['id', 'name', 'credit', 'score', 'category'])
df_doneCourse.head()

for course in doneCourse:
    course_id = course[0]
    if course_id[0:2] == 'CC':
        if course_id[0:4] == 'CCI1':
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'B1'
        elif course_id[0:4] == 'CCI2':
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'B2'
        elif course_id[0:4] == 'CCO3':
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'B3'
        elif course_id[0:4] == 'CCO4':
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'B4'
        elif course_id[0:4] == 'CCC5':
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'B5'
        elif course_id[0:4] == 'CCC6':
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'B6'
    elif course_id[0:2] == 'GR':
        if course_id[2:].isnumeric():
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'AC'
        elif course_id[-2].isalpha():
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'AE'
        else:
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'A3'
    elif course_id[0:2] == 'LI':
        df_doneCourse.loc[doneCourse.index(course), 'category'] = 'C1'
    elif course_id[0:2] == 'SO':
        df_doneCourse.loc[doneCourse.index(course), 'category'] = 'C2'
    elif course_id[0:2] == 'SC':
        df_doneCourse.loc[doneCourse.index(course), 'category'] = 'C3'
    else:
        if course[4] and course_id[:2] == student_aca_code:
            # 若為它系畢修，將視為選修學分
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'A1'
        else:
            df_doneCourse.loc[doneCourse.index(course), 'category'] = 'A2'


all_done_Course = [] #總課表

# 將各 series 轉為 dict 放置 all_course list
for i in range(len(df_doneCourse)):
    tempCourse = df_doneCourse.loc[i,].to_dict()
    all_done_Course.append(tempCourse)

df_doneCourse.loc[:,'credit'] = df_doneCourse['credit'].astype('float')
df_doneCourse.loc[:,'score'] = df_doneCourse['score'].astype('float')

df_doneCourse.loc[df_doneCourse['score'] < 60,'credit'] = 0

# groupby 'category'
df_courseBar = df_doneCourse.groupby('category').sum().credit.to_dict()

# 處理漏掉的項度
cateclass = ['A1', 'A2', 'A3', 'AC', 'AE', 'B1', 'B2','B3','B4','B5','B6', 'C1', 'C2', 'C3']
for cate in [cates for cates in cateclass if cates not in df_courseBar.keys()]:
    df_courseBar[cate] = 0.0

def get_student_course():
    global student_course
    student_course = all_done_Course
    return student_course

def get_student_progress():
    global student_progress
    student_progress = df_courseBar
    return student_progress

# print(get_student_course())
# print('==============================================')
# print(get_student_progress())
# print('==============================================')
# print(student_graduate_info)