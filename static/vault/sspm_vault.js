const parseCookie = str =>
  str
    .split(';')
    .map(v => v.split('='))
    .reduce((acc, v) => {
        acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
        return acc;
    }, {});


function clearCookieAndLogOut() {
    document.cookie = "userToken=0";
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
    if (parsed_cookie["userToken"] == 0) {
        prohibited_page();
    }
}
else {
    prohibited_page();
}

async function fetchCredentials(userToken) {
    try {
        const response = await fetch('/get_creds', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userToken}),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();

        populateList(data);
    } catch (error) {
        console.error('Failed to fetch credentials:', error);
    }
}

function populateList(data) {
    const listContainer = document.getElementById('loginPasswordList');
    listContainer.innerHTML = '';

    data.forEach(({name, login, password}) => {
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
}

const userToken = parseCookie(document.cookie)['userToken'];
fetchCredentials(userToken);
