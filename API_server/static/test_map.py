import folium
import matplotlib.colors as colors
import time
import requests
import random
import json

# URL = "http://localhost:5000/"
URL = "https://plant-humidity-tracker.onrender.com/"


def map_speed_to_color(speed, max_speed):
    color_range = 1
    color = color_range*speed/max_speed
    hex_color = colors.to_hex((color, (color**2)/2, (color**2)/2))
    return hex_color


def get_map_center(coords):
    sum_lat = 0
    sum_lon = 0
    for j in coords:
        i = j[0]
        sum_lat += i[0]
        sum_lon += i[1]

    return sum_lat/len(coords), sum_lon/len(coords)


# Create a list of coordinates that define the line
coords = []
f = open("coords.txt", "r")
max_speed = None
for i in f:
    tmp_coords_arr = i.strip().split(" ")
    line = list(map(float, tmp_coords_arr))
    vel = line[2]
    if max_speed is None or vel > max_speed:
        max_speed = vel
    coords.append([line[:2], vel])

for j in range(len(coords)):
    i = coords[j]
    color = map_speed_to_color(i[-1], max_speed)
    color = "#000000"
    coords[j].append(color)


def generate_map(location, max_count):
    # Create a map centered on the coordinates of interest
    center = get_map_center(coords)
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

    for j in range(len(coords)-1):
        if j >= max_count:
            break
        i = coords[j]
        next_coords = coords[j+1][:1][0]
        color = i[-1]
        i = i[0]
        to_add = [i, next_coords]
        # Create a polyline object with the coordinates
        line = folium.PolyLine(locations=to_add, color=color)

        # Add the polyline to the map
        line.add_to(m)

    # Save the map as an HTML file
    m.save('./map.html')


def simulate_bike_get_lock_state():
    sub_url = "get_data_gps"
    r = requests.get(URL+sub_url).text
    response = json.loads(r)
    return response[0]["locked"]


def simulate_bike_put_data(counter, speed, lat, lon):
    sub_url = "data_post_gps"
    # payload = [{"id": counter ,"locked":lock_state, "lat": i[0], "lon": i[1], "speed": speed}]
    payload = {"id": counter, "lat": lat, "lon": lon, "accuracy": 0, "speed": speed,
                "bat1": 3.7+0.5*random.random(), "bat2": 3.7+0.5*random.random(), "locked": lock_state}
    r = requests.post(URL+sub_url, json=payload).text
    print(r, end=" ")


counter = 0
total_len = 30*60
interval = 10
lock_state = False
while counter < len(coords):
    # lock_state = simulate_bike_get_lock_state()
    lock_state = False
    i = coords[counter][0]
    speed = coords[counter][1]
    print(counter, end=", ")
    print(i, end=", ")
    print(speed)
    generate_map(i, counter)
    counter += (len(coords)//total_len)*interval
    simulate_bike_put_data(counter, speed, i[0], i[1])
    time.sleep(interval)
