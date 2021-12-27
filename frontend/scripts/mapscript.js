//Map:
let mapOptions = {
    center: [49.4768, 8.5155],
    zoom:14.5
}

let map = new L.map('leafletmap', mapOptions);

let layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
map.addLayer(layer);

//Preparation for gliders:
let gliderIcon = {
    iconUrl:"images/glider_icon.png",
    iconSize:[40,40]
}

let gliderIconObj = L.icon(gliderIcon)

let iconOptions = {
    title:"Glider",
    icon:gliderIconObj
}


const marker = {};

function initializeMarkers() {
    for (k in gliders) {
        marker[k] = new L.marker(gliders[k].coordinates, iconOptions);
        marker[k].addTo(map);
        marker[k].bindPopup("ID&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp:&nbsp" + gliders[k].name + "</br> Height: " + gliders[k].height + "&nbsp m</br> Speed: " + gliders[k].speed + "&nbsp m/s");
    }
}

function updateMarker(id) {

}

markerDone = true;
