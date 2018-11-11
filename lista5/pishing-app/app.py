from flask import Flask, request, jsonify
from flask_cors import CORS

import sys

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)


@app.route('/')
def hello():
    return 'jamnik'


@app.route('/push', methods=['POST'])
def parse_pish():
    print(request.get_json(), file=sys.stdout)
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response