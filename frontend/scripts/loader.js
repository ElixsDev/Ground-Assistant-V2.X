var gliders = {
    "a23456": {name: "D-0517", coordinates: [49.4763, 8.515], height: 300, speed: 100},
    "b23456": {name: "D-0518", coordinates: [49.4768, 8.5155], height: 300, speed: 100},
    "c23456": {name: "D-0519", coordinates: [49.4773, 8.516], height: 300, speed: 100}
}

var elements = {
    "1": {name: "D-0518", coordinates: [49.4768, 8.5155], height: 100, speed: 100},
    "2": {name: "D-1230", coordinates: [49.4768, 8.5155], height: 200, speed: 99},
    "3": {name: "D-9930", coordinates: [49.4768, 8.5155], height: 300, speed: 88}
}

updateNextUp();

function setOutOfOrder(what = "all") {
    parent = document.getElementById("main");
    blur = document.createElement("style");
    if (what == "all") {
        blur.innerHTML = `.stats { filter: blur(5px); }
                          .nextup { filter: blur(5px); }
                          .map { filter: blur(5px); }`;
    } else {
        blur.innerHTML = `.${what} { filter: blur(5px); }`;
    }
    parent.appendChild(blur);
}

setOutOfOrder("stats");
//setOutOfOrder("nextup");
