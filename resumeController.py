from flask import Flask, request, jsonify
from ResumeReader import ResumeReader
from ResumeParser import ResumeParser
from Models import Models

app = Flask(__name__)

models = Models()
ner, ner_dates, zero_shot_classifier, tagger = models.load_trained_models()
reader = ResumeReader()
parser = ResumeParser(ner, ner_dates, zero_shot_classifier, tagger) 

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