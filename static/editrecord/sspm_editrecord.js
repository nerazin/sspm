const parseCookie = str =>
  str
    .split(';')
    .map(v => v.split('='))
    .reduce((acc, v) => {
        acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
        return acc;
    }, {});



const form = document.querySelector("#form_elem");

async function sendData() {
    const formData = new FormData(form);
    const jsonObject = {};

    formData.forEach((value, key) => {
        jsonObject[key] = value;
    });
    jsonObject['userid'] = parseCookie(document.cookie)['userToken'];

    var confirm_p = document.getElementById("confirmation_p");
    confirm_p.style.color = "black";
    confirm_p.innerHTML = "Sending...";

    try {
        const response = await fetch('/add_account', {
            method: "POST",
            body: JSON.stringify(jsonObject),
        });
        var responseJson = await response.json();
        console.log(responseJson);

        if (response.ok) {
            confirm_p.innerHTML = "All good! Redirecting...";
            setTimeout(function() {
                window.location.replace("/vault");
            }, 500);
        }
        else {
            console.error("Request failed:", response.status, response.statusText);
            confirm_p.style.color = "red";
            confirm_p.innerHTML = responseJson.message || "An error occurred.";
        }
    }
    catch (e) {
        console.error("Error during fetch:", e);
        confirm_p.style.color = "red";
        confirm_p.innerHTML = "An unexpected error occurred.";
    }
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    sendData();
});