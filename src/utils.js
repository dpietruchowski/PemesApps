function getCookie(input) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var name = cookies[i].split('=')[0].toLowerCase();
        var value = cookies[i].split('=')[1];
        if (name === input) {
            return value;
        } else if (value === input) {
            return name;
        }
    }
    return "";
}

function delete_component(id) {
    fetch("/pricing/component/edit/" + id, {
        method: 'DELETE',
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
    .then(resp => resp.json())
    .then(resp => {
        console.log(resp);
        location.href="/pricing/component/list";
    })
}