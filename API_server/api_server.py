from flask import Flask, json, request, send_from_directory, render_template
from flask_cors import CORS
import folium
import datetime
import random

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
# filename_gps = "log_gps.json"
map_path = "/opt/render/project/src/API_server/templates/map.html"
# map_path = "C:/Users/marek/Documents/Programování/Github/Plant_humidity_tracker/API_server/templates/map.html"
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
    json.dump(incoming_data_gps, open(filename_gps, "w"), indent=4)


def generate_map(location):
    # Create a map centered on the coordinates of interest
    m = folium.Map(
        location=location,
        zoom_start=16,
        tiles='cartodbpositron')

    folium.Marker(location).add_to(m)

    folium.Circle(
        radius=random.random()*100,
        location=location,
        popup="The Waterfront",
        color="#4285F4",
        fill=True,
    ).add_to(m)

    # for j in range(len(coords)-1):
    #     if j >= max_count:
    #         break
    #     i = coords[j]
    #     next_coords = coords[j+1][:1][0]
    #     color = i[-1]
    #     i = i[0]
    #     to_add = [i, next_coords]
    #     # Create a polyline object with the coordinates
    #     line = folium.PolyLine(locations=to_add, color=color)

    #     # Add the polyline to the map
    #     line.add_to(m)

    # Save the map as an HTML file
    # m.save('./templates/map.html')
    print("Saving to", map_path)
    m.save(map_path)


api = Flask(__name__,
            static_url_path="")
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
        location = [incoming["lat"], incoming["lon"]]
        incoming_data_gps.append(incoming)
        json.dump(incoming_data, open(filename_gps, "w"), indent=4)
        print(location)
        generate_map(location)
        return "OK"


@api.route('/data_get_gps', methods=['GET'])
def get_data_gps():
    if request.method == "GET":
        if not incoming_data_gps:
            return None
        return json.dumps(incoming_data_gps[-1])


# HTML page
@api.route('/')
def static_file():
    return render_template("test_sub_page.html")


@api.route('/map')
def static_file_map():
    return render_template("map.html")


if __name__ == '__main__':
    filename = "log.json"
    f = open(filename, "r")
    try:
        incoming_data = json.loads(f.read())
    except:
        incoming_data = []
    api.run(debug=True)
