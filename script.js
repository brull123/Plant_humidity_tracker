const ficus = document.getElementById("ficus_humidity");
const main_url = "https://test-api-gt7l.onrender.com/";
const sub_url = "data";
var URL = main_url + sub_url;

async function change_div() {
    const response = await fetch(URL);
    const jsonData = await response.json();
    var rand_perct = Math.abs(jsonData[1].az*100/9.81);
    if (rand_perct > 100){
        rand_perct = 100;
    }
    ficus.innerText = rand_perct.toFixed(0) + " %";
    ficus.style.width = rand_perct + "%";
    if (rand_perct < 10) {
        ficus.style.color = "black";
    }
    else
        ficus.style.color = "var(--background_white)";

}

setInterval(change_div, 1000);