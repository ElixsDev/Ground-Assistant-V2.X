expected_id = "EDFMglna"
const socket = new WebSocket('wss://eliservices.servehttp.com:5010');

socket.addEventListener('open', function (event) {
    console.log('Connected to server via wss');
    socket.send(expected_id);
});

socket.addEventListener('close', function (event) { console.log('Disconnected from wss'); });

socket.addEventListener('message', function (event) {
    id = event.data.slice(0,8);
    data = event.data.slice(9);

    if (id == expected_id) {
        x = JSON.parse(data);
        console.log(x);
    } else if (id == "_status_") {
        statsupdate(data);
    }
});

function mapupdate(data) {
    console.log(data);
}

function statsupdate(data) {
    console.log(data);
}
