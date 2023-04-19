from flask import Flask, json, request
from flask_cors import CORS

filename = "log.json"
f =  open(filename, "r")
try:
  incoming_data = json.loads(f.read())
except:
  incoming_data = []

api = Flask(__name__)
CORS(api)


@api.route('/data', methods=['GET'])
def get_data():
  if not incoming_data:
    return None
  return json.dumps(incoming_data[-1])

@api.route('/download', methods=['GET'])
def download_data():
  if not incoming_data:
    return None
  return json.dumps(incoming_data)

@api.route('/data_post', methods=['PUT'])
def add_data():
   if request.method == "PUT":
    incoming = request.get_json()
    incoming_data.append(incoming)
    json.dump(incoming_data, open(filename,"w"), indent=4)
    return "OK"


if __name__ == '__main__':
    api.run()