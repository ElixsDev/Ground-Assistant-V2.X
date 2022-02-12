markerDone = false;

//Map:
let mapOptions = {
    center: [49.4768, 8.5155],
    zoom:14.5
}

let map = new L.map('leafletmap', mapOptions);

let layer = new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
map.addLayer(layer);

//Preparation for gliders:
let gliderIcon = L.icon({
    iconUrl: "https://glidertracker.de/img/Glider.png",
    iconSize: [40, 40],
    IconAnchor: [-20, -20]});


const marker = {};
const lastpos = {};
const llastpos = {};
const lastcourse = {};

function updateMarker(id, type, coordinates, registration, speed, height) {
    if (registration == null) { registration = "Unknown"; }
    course = getcourse(id, coordinates);

    info = `${registration} </br>
            Height: ${Math.round(height)}m </br>
            Speed: ${Math.round(speed)}km/h </br>
            Course: ${course}° </br>`;

    if (id in marker) {
        marker[id].setLatLng(coordinates);
        marker[id].setRotationAngle(course);
        marker[id].setPopupContent(info);
        llastpos[id] = lastpos[id];
        lastpos[id] = coordinates;
    } else {
        let iconOptions = { title: type, icon:gliderIcon, rotationAngle: course};
        marker[id] = new L.marker(coordinates, iconOptions);
        marker[id].addTo(map);
        marker[id].bindPopup(info);
        llastpos[id] = coordinates;
        lastpos[id] = coordinates;
    }

}

function getcourse(id, coordinates) {
    if (id in llastpos) {
        diff_N = (coordinates[0] - llastpos[id][0]).toFixed(4);
        diff_E = (coordinates[1] - llastpos[id][1]).toFixed(4);

        if (diff_N > 0 && diff_E == 0) { degree = 0;
        } else if (diff_N > 0 && diff_E > 0) {
            quo = diff_E / diff_N;
            degree = Math.round(Math.atan(quo) * 180 / Math.PI);

        } else if (diff_N == 0 && diff_E > 0) { degree = 90;
        } else if (diff_N < 0 && diff_E > 0) {
            quo = Math.abs(diff_N) / diff_E;
            degree = Math.round(Math.atan(quo) * 180 / Math.PI) + 90;

        } else if (diff_N < 0 && diff_E == 0) { degree = 180;
        } else if (diff_N < 0 && diff_E < 0) {
            quo = Math.abs(diff_N) / Math.abs(diff_E);
            degree = Math.round(Math.atan(quo) * 180 / Math.PI) + 180;

        } else if (diff_N == 0 && diff_E < 0) { degree = 270;
        } else if (diff_N > 0 && diff_E < 0) {
            quo = Math.abs(diff_E) / diff_N;
            degree = Math.round(Math.atan(quo) * 180 / Math.PI) + 90;

        } else if (diff_N == 0 && diff_E == 0) {
            if (id in lastcourse) { degree = lastcourse[id]; }
            else { degree = 0; }
        }

        lastcourse[id] = degree;
        return degree;

    } else { return 0; }
}

markerDone = true;
