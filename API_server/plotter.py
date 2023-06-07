import json
import matplotlib.pyplot as plt
import os
import datetime
from time import sleep

os.chdir("API_server")
filename = "log.json"
f = open(filename, "r").read()
log_dict = json.loads(f)
x_ax = []
y_ax = []
for j in range(len(log_dict)):
    i= log_dict[j]
    if "time" in i:
        # i["time"] = "'2023-10-11 5:00:10.000000'"
        t = datetime.datetime.strptime(i["time"][1:-8], "%Y-%m-%d %H:%M:%S")
        x_ax.append(t)
        perct = (4096-i["hum"])*100/4096
        y_ax.append(perct)


def watering_detection(x_ax, y_ax, threshold = 5):
    last = None
    waterings = []
    for i in range(len(x_ax)):
        current = y_ax[i]
        if last is not None:
            diff = current - last
            if diff > threshold:
                waterings.append(x_ax[i])
        last = current
    plt.vlines(waterings, 0, 100, colors=["black"], linestyles=["dashed"])


watering_detection(x_ax, y_ax, threshold = 10)
plt.plot(x_ax, y_ax)
plt.ylim([0, 100])
plt.grid()
plt.ylabel("Humidity [%]")
plt.xlabel("Date")
plt.title("Soil humidity")
plt.show()