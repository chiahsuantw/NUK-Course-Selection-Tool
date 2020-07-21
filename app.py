from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

'''
with open(r'static\json\courseData.json', 'r', encoding='utf-8-sig') as jsonFile:
    courseData = json.load(jsonFile)
'''

url = 'https://c1a29eb6-2be3-428b-8cbb-079ffd3a058d.mock.pstmn.io/courseData'
response = requests.get(url)
courseData = json.loads(response.text)

@app.route('/')
def index():
    return render_template('index.html', courseData=courseData)

if __name__ == "__main__":
    app.run(debug=True)