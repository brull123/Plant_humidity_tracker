from flask import Flask, json, request
from flask_cors import CORS
import datetime

# Plant humidity tracker
filename_git = "log.json"
filename = "/API/data/log_render.json"
# filename = "log.json"
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
    json.dump(incoming_data, open(filename_git, "w"), indent=4)

filename_git_gps = "log_gps.json"
filename_gps = "/API/data/log_render_gps.json"
# filename = "log_gps.json"
try:
    f = open(filename_gps, "r")
    incoming_data_gps = json.loads(f.read())
    print("Log found")
except:
    print("No log found")
    try:
        f = open(filename_git_gps, "r")
        incoming_data_gps = json.loads(f.read())
        print("Copying log from git")
    except:
        incoming_data_gps = []
        print("Creating empty log")
    json.dump(incoming_data_gps, open(filename_git_gps, "w"), indent=4)


api = Flask(__name__)
CORS(api)

# Plant humidity tracker
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

# GPS tracker
@api.route('/data_post_gps', methods=['POST'])
def add_data_gps():
    now = json.dumps(datetime.datetime.now(), default=str)
    if request.method == "POST":
        incoming = request.get_json()
        print(incoming)
        # incoming["time"] = now
        incoming_data_gps.append(incoming)
        return "OK"

@api.route('/data_get_gps', methods=['GET'])
def get_data_gps():
    if request.method == "GET":
        if not incoming_data_gps:
            return None
        return json.dumps(incoming_data_gps[-1])



if __name__ == '__main__':
    filename = "log.json"
    f = open(filename, "r")
    try:
        incoming_data = json.loads(f.read())
    except:
        incoming_data = []
    api.run()
