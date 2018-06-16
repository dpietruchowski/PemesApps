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