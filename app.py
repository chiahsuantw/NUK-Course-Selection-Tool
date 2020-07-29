from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

'''
with open('static\\json\\course.json', 'r', encoding='utf-8-sig') as jsonFile:
    courseData = json.load(jsonFile)
'''

url = 'https://0bdba922-52eb-483b-b4ea-5a066c1f22df.mock.pstmn.io/courseData'
response = requests.get(url)
courseData = json.loads(response.text)


@app.route('/')
def index():
    return render_template('index.html', courseData=courseData)

if __name__ == "__main__":
    app.run(debug=True)