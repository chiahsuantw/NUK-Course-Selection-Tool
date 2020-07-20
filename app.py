from flask import Flask, render_template
import json

app = Flask(__name__)

with open(r'static\json\courseData.json', 'r', encoding='utf-8-sig') as jsonFile:
    courseData = json.load(jsonFile)

@app.route('/')
def index():
    return render_template('index.html', courseData=courseData)

if __name__ == "__main__":
    app.run(debug=True)