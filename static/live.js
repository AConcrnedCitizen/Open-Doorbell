$(document).ready(function () {
    //connect to the socket server.
    var x = document.getElementById("audio"); 
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/live');
    //receive details from server
    socket.on('buttonpressed', function (msg) {
        console.log(msg);
        x.play();
        Notification.requestPermission().then(perm => {
            if (perm === "granted") {
                new Notification("Doorbell Rung");
            }
        })
    });

});