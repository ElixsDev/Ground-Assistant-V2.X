const socket = new WebSocket('wss://eliservices.servehttp.com:5010');

socket.addEventListener('open', function (event) { console.log('Connected to WS Server!'); });
socket.addEventListener('close', function (event) { console.log('Disconnected from the WS Server!'); });

socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
});
