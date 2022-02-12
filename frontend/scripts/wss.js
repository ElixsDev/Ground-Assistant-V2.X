expected_id = "EDFMglna"
const socket = new WebSocket('wss://eliservices.servehttp.com:5010');

socket.addEventListener('open', function (event) {
    console.log('Connected to server via wss');
    socket.send(expected_id);
});

socket.addEventListener('close', function (event) {
    console.log('Disconnected from wss');
    alert(`DatenServer offline, mögliche Gründe:
       * Der Server ist nur zwischen 5 und 24 Uhr UTC erreichbar
       * Wartungsarbeiten`);
});

socket.addEventListener('message', function (event) {
    id = event.data.slice(0,8);
    data = event.data.slice(9);

    if (id == expected_id) {
        x = JSON.parse(data);
        if (markerDone) {
            for (index in x) {
                plane = x[index]
                //console.log(plane["turn_rate"])
                updateMarker(plane["device_id"], plane["type"], [plane["latitude"], plane["longitude"]],
                             plane["registration"], plane["ground_speed"], plane["altitude"]);
            }
        }
    } else if (id == "_status_") {
        statsupdate(data);
    }
});

function statsupdate(data) {
    console.log(data);
}

