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


const dataFromServer = [
    {name: 'John Doe', login: 'User1', password: 'password1'},
    {name: 'Jane Smith', login: 'User2', password: 'password2'},
    {name: 'Alice Johnson', login: 'User3', password: 'password3'},
];

const listContainer = document.getElementById('loginPasswordList');

dataFromServer.forEach(({ name, login, password }) => {
    const item = document.createElement('div');
    item.className = 'list_item';
    item.innerHTML = `
        <span class="name">${name}</span>
        <div class="login-password">
            <span class="login">${login}</span>
            <span class="password">${password}</span>
        </div>
    `;
    listContainer.appendChild(item);
});

