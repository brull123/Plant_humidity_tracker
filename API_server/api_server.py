from flask import Flask, json, request
from flask_cors import CORS
import datetime

filename_git = "log.json"
filename = "/API/data/log_render.json"
try:
    f = open(filename, "r")
    incoming_data = json.loads(f.read())
    print("Log found")
except:
    print("No log found")
    try:
        f = open(filename_git, "r")
        incoming_data = json.loads(f.read())
        print("Copying log from git")
    except:
        incoming_data = []
        print("Creating empty log")
    json.dump(incoming_data, open(filename, "w"), indent=4)


api = Flask(__name__)
CORS(api)


@api.route('/data', methods=['GET'])
def get_data():
    global incoming_data
    print(incoming_data[-1])
    return json.dumps(incoming_data[-1])


@api.route('/download', methods=['GET'])
def download_data():
    if not incoming_data:
        return None
    return json.dumps(incoming_data)


@api.route('/data_post', methods=['PUT'])
def add_data():
    now = json.dumps(datetime.datetime.now(), default=str)
    if request.method == "PUT":
        incoming = request.get_json()
        incoming["time"] = now
        incoming_data.append(incoming)
        json.dump(incoming_data, open(filename, "w"), indent=4)
        return "OK"

@api.route('/data_post_2', methods=['POST'])
def add_data():
    if request.method == "POST":
        print("Received data")
        print(request.get_json())
        return "OK"


if __name__ == '__main__':
    filename = "log.json"
    f = open(filename, "r")
    try:
        incoming_data = json.loads(f.read())
    except:
        incoming_data = []
    api.run()
