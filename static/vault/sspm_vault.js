const parseCookie = str =>
  str
    .split(';')
    .map(v => v.split('='))
    .reduce((acc, v) => {
        acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
        return acc;
    }, {});


function clearCookieAndLogOut() {
    document.cookie = name+'logged_in=0';
    window.location.replace("/");
}


var allow_p = document.getElementById("allow_p");

try {
    var parsed_cookie = parseCookie(document.cookie);    
}
catch (e) {
    parsed_cookie = false;
}

if (parsed_cookie) {
    if (parsed_cookie["logged_in"] == 1) {
        allow_p.style.color = "Green";
        allow_p.innerHTML = "You are allowed!";
    }
    else {
        allow_p.style.color = "red";
        allow_p.innerHTML = "You are not allowed!";
    }
}
else {
    allow_p.style.color = "red";
    allow_p.innerHTML = "You are not allowed!";
}
