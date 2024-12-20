var map = L.map('map').setView([48.8566, 2.3522], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

map.on('click', function(e) {
    var latlng = e.latlng;
    var lat = latlng.lat;
    var lng = latlng.lng;

    document.getElementById("departure").value = lat + ", " + lng;

    L.marker([lat, lng]).addTo(map)
        .bindPopup("Selected Departure")
        .openPopup();
});
