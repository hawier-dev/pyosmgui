var map = L.map('map').setView([51.505, -0.09], 13);
var currentCursorLocation = null;
var markers = [];
var currentLocationMarker = null;

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

map.on('mousemove', function(e) {
    currentCursorLocation = e.latlng;
});

map.on('zoomend', function() {
    var zoomLevel = map.getZoom();
    console.log("zoom_level:" + zoomLevel);
})

document.getElementById('locate-me').addEventListener('click', function() {
    map.locate({setView: true, maxZoom: 16});
});

function getCurrentLocation() {
    var center = map.getCenter();
    return [center.lat, center.lng];
}

function getCurrentCursorLocation() {
    console.log("mouse_move:" + currentCursorLocation.lat + ", " + currentCursorLocation.lng);
}

function resizeMap(height) {
    document.getElementById('map').style.height = height + 'px';
    map.invalidateSize();
}

function goToLocation(lat, lng, zoom) {
    map.setView([lat, lng], zoom);
}

function addCurrentLocationMarker(lat, lng, popupText, iconUrl, iconSize) {
    if (currentLocationMarker) {
        map.removeLayer(currentLocationMarker);
    }
    iconSize = iconSize !== "None" ? iconSize : [25, 41];
    console.log("iconUrl: " + iconUrl + ", iconSize: " + iconSize);
    if (iconUrl == "None" || iconSize == "None") {
        currentLocationMarker = L.marker([lat, lng]);
    }
    else {
        var icon = L.icon({
            iconUrl: iconUrl,
            iconSize: iconSize,
        });
        currentLocationMarker = L.marker([lat, lng], {icon: icon});
    }
    map.addLayer(currentLocationMarker);
    currentLocationMarker.bindPopup(popupText).openPopup();
    goToLocation(lat, lng, 16);
}

function addMarker(lat, lng, popupText = null) {
    if (iconUrl == "None" || iconSize == "None") {
        var marker = L.marker([lat, lng]);
    }
    else {
        var icon = L.icon({
            iconUrl: iconUrl,
            iconSize: iconSize,
        });
        var marker = L.marker([lat, lng], {icon: icon});
    }

    marker.addLayer(marker);
    if (popupText) {
        marker.bindPopup(popupText).openPopup();
    }
    markers.push(marker);
}


function removeMarkerByIndex(index) {
    map.removeLayer(markers[index]);
    markers.splice(index, 1);
}

function removeAllMarkers() {
    for (var i = 0; i < markers.length; i++) {
        map.removeLayer(markers[i]);
    }
    markers = [];
}