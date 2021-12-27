function fileExists(urlToFile) {
    var xhr = new XMLHttpRequest();
    xhr.open('HEAD', urlToFile, false);
    xhr.send();

    if (xhr.status == "404") { return false; }
    else { return true; }
}


function updateNextUp() {
    for (k in elements) {
        imgLink ='images/planes/' + elements[k].name + '.png';

        if ( ! fileExists(imgLink) ) {
            imgLink = 'images/planes/unknown.png';
        }

        positions[k].image.src = imgLink;
        positions[k].name.textContent = elements[k].name;
        positions[k].height.textContent = elements[k].height + "m";
        positions[k].time.textContent = "5" + "s";
    }
}


var positions = {
    "1": {image: document.getElementById('image1'), name: document.getElementById('name1'), height: document.getElementById('height1'), time: document.getElementById('time1')},
    "2": {image: document.getElementById('image2'), name: document.getElementById('name2'), height: document.getElementById('height2'), time: document.getElementById('time2')},
    "3": {image: document.getElementById('image3'), name: document.getElementById('name3'), height: document.getElementById('height3'), time: document.getElementById('time3')}
}

var nextupDone = true;
