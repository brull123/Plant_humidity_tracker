import requests
import json
import datetime
import time
import os

# main_url = "http://localhost:5000/"
main_url = "https://plant-humidity-tracker.onrender.com/"

def get_last():
    sub_url = "data"
    URL = main_url + sub_url
    r = requests.get(url=URL).text
    # response = json.loads(r)
    print(r)

def download_data():
    os.chdir("./API_server")
    filename = "log.json"
    sub_url = "download"
    URL = main_url + sub_url

    r = requests.get(url=URL).text
    response = json.loads(r)
    json.dump(response, open(filename,"w"), indent=4)
    for i in response:
        print(i)

def test_put(runs = None):
    sub_url = "data_post"
    URL = main_url + sub_url
    if runs is None:
        while True:
            now = json.dumps(datetime.datetime.now(), default=str)
            payload = {"id":0, "hum": 3600}
            r_2 = requests.put(URL, json=payload).text
            print(r_2, end=" ")
            print(now)
            time.sleep(5)
    else:
        for i in range(runs):
            now = json.dumps(datetime.datetime.now(), default=str)
            payload = {"id":0, "hum": 3600}
            r_2 = requests.put(URL, json=payload).text
            print(r_2, end=" ")
            print(now)
            time.sleep(5)


if __name__=="__main__":
    # test_put(5)
    # get_last()
    download_data()
