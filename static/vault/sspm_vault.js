const parseCookie = str =>
  str
    .split(';')
    .map(v => v.split('='))
    .reduce((acc, v) => {
        acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
        return acc;
    }, {});


function clearCookieAndLogOut() {
    document.cookie = "logged_in=0";
    window.location.replace("/");
}

try {
    var parsed_cookie = parseCookie(document.cookie);    
}
catch (e) {
    parsed_cookie = false;
}

function prohibited_page() {
    var newContent="<h1>Access Denied. Redirecting to the login page...</h1>";
    document.open();
    document.write(newContent);
    document.close();

    setTimeout(function() {
        window.location.replace("/");
    }, 2000);
}

if (parsed_cookie) {
    if (parsed_cookie["logged_in"] != 1) {
        prohibited_page();
    }
}
else {
    prohibited_page();
}
