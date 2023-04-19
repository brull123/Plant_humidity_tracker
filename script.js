const ficus = document.getElementById("ficus_humidity");

async function change_div() {
    var rand_perct = Math.random() * 100;
    ficus.innerText = rand_perct.toFixed(0) + " %";
    ficus.style.width = rand_perct + "%";
    if (rand_perct < 10) {
        ficus.style.color = "black";
    }
    else
        ficus.style.color = "var(--background_white)";

}

// setInterval(change_div, 1000);