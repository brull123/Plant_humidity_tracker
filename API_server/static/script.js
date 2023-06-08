const lat_element = document.getElementById("location-lat");
const lon_element = document.getElementById("location-lon");
const speed_element = document.getElementById("location-speed");
const map_element = document.getElementById("map");
const stolen_element = document.getElementById("stolen");
const lock_element = document.getElementById("lock");
const button_lock_element = document.getElementById("button-lock");
const bat1_element = document.getElementById("bat1");
const bat2_element = document.getElementById("bat2");
var lock_state = false;
var locked_val = false;

const main_url = "https://plant-humidity-tracker.onrender.com/";

// const main_url = "http://localhost:5000/";
var first_load = true;

async function change_div() {
    // var sub_url = "data";
    var sub_url = "data_get_gps";
    var URL = main_url + sub_url;
    const response = await fetch(URL);
    const jsonData = await response.json();
    console.log(jsonData);
    var lat_val = jsonData.lat;
    var lon_val = jsonData.lon;
    // var speed_val = jsonData.speed;
    // locked_val = jsonData.locked;
    var bat1_val = jsonData.bat1;
    var bat2_val = jsonData.bat2;

    lat_element.innerText = lat_val.toFixed(5);
    lon_element.innerText = lon_val.toFixed(5);
    // speed_element.innerText = speed_val.toFixed(2) + " km/h";
    // if (locked_val && speed_val > 1) {
    //     stolen_element.innerText = "Stolen";
    // } else {
    //     stolen_element.innerText = "Safe";
    // }
    // lock_element.innerText = locked_val;
    // if (locked_val) {
    //     if (locked_val == lock_state) {
    //         button_lock_element.innerText = "Unlock";
    //     }
    //     lock_element.innerText = "Locked";
    //     if (first_load) {
    //         lock_state = locked_val;
    //         button_lock_element.style.background = "#FF0000"
    //         button_lock_element.innerText = "Unlock";
    //         first_load = false;
    //     }
    // } else {
    //     lock_element.innerText = "Unlocked";
    //     if (locked_val == lock_state) {
    //         button_lock_element.innerText = "Lock";
    //     }
    //     if (first_load) {
    //         lock_state = locked_val;
    //         button_lock_element.style.background = "#4CAF50"
    //         button_lock_element.innerText = "Lock";
    //         first_load = false;
    //     }
    // }
    map_element.setAttribute('src', main_url + "map")
    // map_element.setAttribute('src', "http://127.0.0.1:5000/map")
    bat1_element.innerText = bat1_val.toFixed(2) + " V";
    bat2_element.innerText = bat2_val.toFixed(2) + " V";
}
change_div();

async function lock_state_set() {
    lock_state = !lock_state;
    if (lock_state) {
        console.log(lock_state);
        console.log(locked_val);
        if (lock_state != locked_val) {
            button_lock_element.innerText = "Locking";
        } else {
            button_lock_element.innerText = "Unlock";
        }
        button_lock_element.style.background = "#FF0000"
    } else {
        if (lock_state != locked_val) {
            button_lock_element.innerText = "Unlocking";
        } else {
            button_lock_element.innerText = "Lock";
        }
        button_lock_element.style.background = "#4CAF50"
    }
    var sub_url = "put_data_web";
    var URL = main_url + sub_url;
    var dataObject = [{ id: 0, locked: lock_state }];
    const response = await fetch(URL, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataObject)
    })
}

setInterval(change_div, 10000);