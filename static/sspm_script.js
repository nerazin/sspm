function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

var s = document.getElementById("js_randnum");
s.innerHTML = getRandomInt(10);
