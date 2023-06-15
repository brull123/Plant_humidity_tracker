from flask import Flask, json, request, send_from_directory, render_template
from flask_cors import CORS
import folium
import datetime
import random
from math import sin, cos, sqrt, atan2, radians


# Plant humidity tracker
filename_git = "log.json"
# filename = "/API/data/log_render.json"
filename = "log.json"
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
# filename_gps = "/API/data/log_render_gps.json"
filename_gps = "log_gps.json"
# map_path_dir = "/opt/render/project/src/API_server/templates/"
map_path_dir = "./templates/"
map_path = map_path_dir + "map.html"
# map_path = "C:/Users/marek/Documents/Programování/Github/Plant_humidity_tracker/API_server/templates/map.html"

lock_state = None
location_locked = None

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


def log_to_coords(log):
    coords = []
    for i in log:
        if "lat" in i and "lon" in i:
            lat = i["lat"]
            lon = i["lon"]
            coords.append([lat, lon])
    return coords


def distance_from_coords(current, last):

    R = 6378.0

    lat1, lon1 = current
    lat2, lon2 = last

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def generate_map(location):  # , location_locked):
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

    if lock_state and location_locked is not None:
        folium.Circle(
            radius=200,
            location=location_locked,
            popup="The Waterfront",
            color="#900C3F",
            fill=True,
        ).add_to(m)

    coords = log_to_coords(incoming_data_gps)

    for j in range(len(coords)-1):
        i = coords[j]
        next_coords = coords[j+1]
        # next_coords = coords[j+1][:1][0]
        color = "#000000"
        # i = i[0]
        if i != [0, 0] and next_coords != [0, 0]:
            to_add = [i, next_coords]
        # print(to_add)
        # Create a polyline object with the coordinates
        line = folium.PolyLine(locations=to_add, color=color)

        # Add the polyline to the map
        line.add_to(m)

    # Save the map as an HTML file
    # m.save('./templates/map.html')
    # print("Saving to", map_path)
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
        incoming["locked"] = lock_state
        last = log_to_coords(incoming_data_gps)
        if last:
            last = log_to_coords(incoming_data_gps)[-1]
        incoming["time"] = now
        if lock_state and location_locked is not None:
            dist = distance_from_coords(location, location_locked)
            # print("Printing distance")
            # print(dist)
            if dist > 10:
                incoming["stolen"] = True
        if last:
            last_entry = incoming_data_gps[-1]

            t_now = datetime.datetime.strptime(
                str(now.split(".")[0])[1:], '%Y-%m-%d %H:%M:%S')
            t_last = datetime.datetime.strptime(
                str(last_entry["time"].split(".")[0])[1:], '%Y-%m-%d %H:%M:%S')
            time_diff = abs(t_last-t_now).total_seconds()
            dist = distance_from_coords(location, last)
            # print(dist)
            speed = 3.6*dist / time_diff
            # print(speed)
            incoming["speed"] = speed
        incoming_data_gps.append(incoming)
        json.dump(incoming_data, open(filename_gps, "w"), indent=4)
        # print(location)

        generate_map(location)
        return "OK"


@api.route('/data_post_web', methods=['POST'])
def add_data_web():
    global lock_state
    global location_locked
    incoming = request.get_json()
    lock_state = incoming[0]["locked"]
    if lock_state:
        location_locked = [incoming_data_gps[-1]
                           ["lat"], incoming_data_gps[-1]["lon"]]
    # print(lock_state)
    # print(location_locked)
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
    return send_from_directory(map_path_dir, "map.html")
    # return render_template("map.html")


if __name__ == '__main__':
    filename = "log.json"
    f = open(filename, "r")
    try:
        incoming_data = json.loads(f.read())
    except:
        incoming_data = []
    api.run(debug=True)
