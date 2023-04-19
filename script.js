const ficus = document.getElementById("ficus_humidity");
const main_url = "https://plant-humidity-tracker.onrender.com/";
const sub_url = "data";
var URL = main_url + sub_url;

async function change_div() {
    const response = await fetch(URL);
    const jsonData = await response.json();
    var rand_perct = Math.abs(100*(1-jsonData.hum/4096));
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
change_div();
setInterval(change_div, 5000);