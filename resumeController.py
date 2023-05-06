from flask import Flask, request, jsonify
from ResumeReader import ResumeReader
from ResumeParser import ResumeParser
from Models import Models
import os
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/py/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

models = Models()
ner, ner_dates, zero_shot_classifier, tagger = models.load_trained_models()
reader = ResumeReader()
parser = ResumeParser(ner, ner_dates, zero_shot_classifier, tagger) 

@app.route('/py/parse_cv_and_job', methods=['POST'])
def parse_cv_and_job():

    file = request.files['cv']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    file_path = os.path.join(app.root_path, 'uploads', file.filename)
    cv_text = reader.read_file(file_path)

    job_desc = request.form['job_desc']
    print('job_desc--', job_desc)
    # job_desc_converted = json.loads(job_desc.decode('utf-8'))

    data = parser.parse(cv_text, job_desc)

    return jsonify(data)

@app.route('/py/', methods=['GET'])
def hello():
    return 'App is running'

if __name__ == '__main__':
    app.run()