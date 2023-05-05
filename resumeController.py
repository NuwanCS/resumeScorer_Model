from flask import Flask, request, jsonify
from pyresparser import ResumeParser

app = Flask(__name__)
parser = ResumeParser()

@app.route('/py/parse_cv_and_job', methods=['POST'])
def parse_cv_and_job():
    cv = request.files['cv']

    job_desc = request.form['job_desc']

    data = parser.parse(cv, job_desc)

    return jsonify(data)
@app.route('/py/', methods=['GET'])
def hello():
    return 'App is running'

if __name__ == '__main__':
    app.run()