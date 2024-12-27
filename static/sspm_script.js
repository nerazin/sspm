// document.getElementById('form_elem').addEventListener('submit', function(event) {
//     event.preventDefault(); // Prevent the default form submission

//     const form = event.target;
//     const formData = new FormData(form); // Collect form data
//     const jsonObject = {};

//     // Convert FormData to a JSON object
//     formData.forEach((value, key) => {
//         jsonObject[key] = value;
//     });

//     // Example: Sending JSON data via fetch
//     fetch('/checklogin', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(jsonObject),
//     })
//     .then(response => response.json());
//     // .then(data => console.log('Success:', data));
//     // .catch(error => console.error('Error:', error));
// });


// function getRandomInt(max) {
//     return Math.floor(Math.random() * max);
// }

// var s = document.getElementById("js_randnum");
// s.innerHTML = getRandomInt(10);



// window.location.replace("/vault");


const form = document.querySelector("#form_elem");
const unlockButton = document.getElementById('unlock_button');
const registerButton = document.getElementById('register_button');
// let targetEndpoint = "/checklogin";

async function sendData(targetEndpoint) {
    const formData = new FormData(form);
    const jsonObject = {};

    formData.forEach((value, key) => {
        jsonObject[key] = value;
    });

    var confirm_p = document.getElementById("confirmation_p");
    confirm_p.style.color = "black";
    confirm_p.innerHTML = "Sending...";


    try {
        const response = await fetch(targetEndpoint, {
            method: "POST",
            body: JSON.stringify(jsonObject),
        });
        var responseJson = await response.json();
        console.log(responseJson);


        if (response.ok) {
            if (targetEndpoint === '/checklogin') {
                document.cookie = `userToken=${responseJson["userid"]}`;
                confirm_p.style.color = "green";
                confirm_p.innerHTML = "All good! Redirecting...";
                setTimeout(function() {
                    window.location.replace("/vault");
                }, 500);
            }
            else if (targetEndpoint === "/register") {
                document.cookie = `userToken=${responseJson["userid"]}`;
                confirm_p.style.color = "green";
                confirm_p.innerHTML = "Registration successful! Redirecting...";   
                setTimeout(function() {
                    window.location.replace("/vault");
                }, 500);
            }
        }
        else if (response.status === 401) {
            console.error("Login failed:", response.status, response.statusText);
            confirm_p.style.color = "red";
            confirm_p.innerHTML = "Incorrect login or pass";
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
    const targetEndpoint = event.submitter.id === "unlock_button"
        ? "/checklogin"
        : "/register";
    sendData(targetEndpoint);
});