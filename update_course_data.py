import json

import bs4
import pandas as pd
import requests

currentYear = 110
currentSemester = 1

Sclass = ['AM', 'LI', 'GL', 'IN', 'CCD', 'FI', 'AE', 'AB', 'LS', 'CDA', 'SC', 'WL', 'AP', 'GR', 'CCM', 'TODO',
          'EL', 'KH', 'CS', 'IFD', 'IM', 'SO', 'AC', 'CD', 'CHS', 'FL', 'CC', 'EE', 'DA', 'DAP', 'CE', 'CM', 'LA']

class_code = json.load(open('class_code.json', 'r', encoding='utf-8'))


def scrap_all_course():
    all_course = []  # 總課表

    for sclass in Sclass:
        data = '<tr><td+width=""33%"">開課學年：' + str(currentYear) + '　　開課學期：第' + str(currentSemester) + \
               '學期</td><td+width=""33%"">開課部別：大學部</td><td+width=""34%"">開課系所：無</td></tr><tr><td+width=""33%"">' \
               '開課班級：無</td><td+width=""33%"">授課教師：無</td><td+width=""34%"">上課時間：無</td></tr>'

        req = requests.post('https://course.nuk.edu.tw/QueryCourse/QueryResult.asp',
                            data={'Condition': data, 'Flag': 1, 'OpenYear': currentYear,
                                  'Helf': currentSemester, 'Pclass': 'A', 'Sclass': sclass,
                                  'Yclass': '', 'SirName': '', 'Sirno': '', 'WeekDay': '',
                                  'Card': '', 'Subject': '', 'Language': '', 'Pre_Cono': '',
                                  'Coname': ''})
        req.encoding = 'utf8'
        soup = bs4.BeautifulSoup(req.text, 'html.parser')
        soup = soup.find_all('tr')

        # i 是要略過非課程的資料
        i = 0

        for ele in soup:
            if i <= 3:
                i += 1
                continue
            tdSet = ele.find_all('td')

            # 微學分奇怪的格式 (判斷 : 學分未滿 1 但大於 0)
            if 1.0 > float(tdSet[6].text.upper()) > 0.0:
                continue  # 略過囉

            # 存取課程的詳細資料[id, dept, name, grade, class, teacher, period, category, credit, location]
            tempCourse = {'id': tdSet[0].text.upper() + tdSet[1].text.upper(), 'dept': sclass, 'name': tdSet[5].text,
                          'grade': tdSet[3].text, 'class': tdSet[4].text,
                          'teacher': tdSet[12].decode_contents()[0:-5].replace('<br/>', ',')}

            # 課程時間處理 以 list 存放多個時段
            course_time = []
            for i in range(14, 21):
                try:
                    if tdSet[i].text != '\u3000':  # 編碼問題
                        for day in tdSet[i].text.split(','):
                            if day == 'X':
                                course_time.append([i - 13, 0])
                            elif day == 'Y':
                                course_time.append([i - 13, 4.5])  # 中午顯示 4.5
                            else:
                                try:
                                    course_time.append([i - 13, int(day)])
                                except ValueError:
                                    print("[Scraper] Convert to int error: {}".format(day))  # 印出錯誤格式
                                    pass
                except Exception as e:
                    print(e)
                    print("[Scraper] list out of index", tdSet[5].text)

            tempCourse['period'] = course_time
            # 必修以 True 表示, 選修以 False
            if tdSet[7].text == '必':
                tempCourse['category'] = True
            else:
                tempCourse['category'] = False
            tempCourse['credit'] = tdSet[6].text
            tempCourse['location'] = tdSet[13].text

            # 放入字典
            all_course.append(tempCourse)

    return all_course


def data_process(data):
    """
    A1 系上必修 :
    A2 系上選修 :
    A3 共同必修 : 'GR'

    B1 核心通識 思維方法 : 'CC'
    B2 核心通識 美學素養 : 'CC'
    B3 核心通識 公民素養 : 'CC'
    B4 核心通識 文化素養 : 'CC'
    B5 核心通識 科學素養 : 'CC'
    B6 核心通識 倫理素養 : 'CC'

    C1 博雅通識 人文科學 : 'LI'
    C2 博雅通識 社會科學 : 'SO'
    C3 博雅通識 自然科學 : 'SC'
    :param data: DataFrame (pandas)
    :return all_course: dictionary
    """

    # 做 A,C 的分類
    data.loc[data.dept == 'LI', 'category'] = 'C1'
    data.loc[data.dept == 'SO', 'category'] = 'C2'
    data.loc[data.dept == 'SC', 'category'] = 'C3'
    data.loc[data.dept == 'GR', 'category'] = 'A3'
    data.loc[data.dept == 'CC', 'category'] = 'B'
    data.loc[data.category == True, 'category'] = 'A1'
    data.loc[data.category == False, 'category'] = 'A2'

    # 做 B 的細類
    # [I1, I2, O3, O4, C5, C6]
    C5 = []
    C6 = []
    I1 = []
    I2 = []
    O3 = []
    O4 = []

    # df_allCourse.id = 'CCXXXXX'
    for dd in data.id:
        I1.append(dd[:4] == 'CCI1')
        I2.append(dd[:4] == 'CCI2')
        O3.append(dd[:4] == 'CCO3')
        O4.append(dd[:4] == 'CCO4')
        C5.append(dd[:4] == 'CCC5')
        C6.append(dd[:4] == 'CCC6')
    # CC 內放置各向度的真值表
    CC = [I1, I2, O3, O4, C5, C6]
    # .loc[bool_list, column_name] 將會把 bool_list中為True的rows拿出來
    for i in range(0, 6):
        data.loc[CC[i], 'category'] = 'B' + str(i + 1)

    # repeat 為表示合開課堂
    repeat = data[data.duplicated(subset=['id', 'grade', 'location', 'teacher', 'dept'], keep='first')]
    # 將電機重複項存入 B_class_repeat
    B_class_repeat = list(repeat.index)
    # 使用 loc 更改 B -> AB
    data.loc[B_class_repeat, 'class'] = 'AB'
    # 移除重複項
    data.drop_duplicates(subset=['id', 'grade', 'location', 'teacher'], keep='last', inplace=True)

    course_dept = list(set(data.dept))

    # 移除電機土環
    course_dept.remove('CE')
    course_dept.remove('EE')

    # 移除非 AB 系統的科系
    for cd in course_dept:
        data.loc[data.dept == cd, 'class'] = ''

    all_course = []  # 總課表

    # 重整 id 順序
    data.reset_index(drop=True, inplace=True)

    # 將各 series 轉為 dict 放置 all_course list
    for i in range(len(data)):
        temp_course = data.loc[i,].to_dict()
        all_course.append(temp_course)

    return all_course


if __name__ == '__main__':
    course_data = scrap_all_course()
    df_all_course = pd.DataFrame(course_data)
    process_data = data_process(df_all_course)

    # 存入 course_data.json
    with open('course_data.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(process_data, ensure_ascii=False))
