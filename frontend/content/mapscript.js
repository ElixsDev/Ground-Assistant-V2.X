let mapOptions = {
    center: [49.4768, 8.5155],
    zoom:14.5
}

let map = new L.map('leafletmap', mapOptions);

let layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
map.addLayer(layer);
