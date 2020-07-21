from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

'''
with open('static\\json\\courseData.json', 'r', encoding='utf-8-sig') as jsonFile:
    courseData = json.load(jsonFile)
'''

url = 'https://2d2650ce-c3e3-48f9-83e1-afef9c66b563.mock.pstmn.io/courseData'
response = requests.get(url)
courseData = json.loads(response.text)

@app.route('/')
def index():
    return render_template('index.html', courseData=courseData)

if __name__ == "__main__":
    app.run(debug=True)