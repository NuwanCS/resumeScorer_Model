from flask import Flask, request, jsonify
from pyresparser import ResumeParser

app = Flask(__name__)
parser = ResumeParser()

@app.route('/parse_cv', methods=['POST'])
def parse_cv():
    cv = request.files['cv']
    data = parser.parse(cv)
    return jsonify(data)

if __name__ == '__main__':
    app.run()