// const center = L.LatLng(23,773, 120);
const center = [24.998357333095207, 121.57946295231254];

const map = L.map('map', {
    center: center, // 中心點座標
    zoom: 15, // 0 - 18
    attributionControl: true, // 是否秀出「leaflet」的貢獻標記
    zoomControl: true , // 是否秀出 - + 按鈕
});
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
// }).addTo(map);
// mbtiles = mbtiles('TaiwanEMap.mbtiles');
const mb = L.tileLayer.mbTiles("./TaiwanEMap.mbtiles").addTo(map);

mb.on('databaseloaded', function(ev) {
    console.info('MBTiles DB loaded', ev);
});
mb.on('databaseerror', function(ev) {
    console.info('MBTiles DB error', ev);
});


function onMarkerClick(){
    this.openPopup();
}

function onMapClick(e) {
    let lat = e.latlng.lat; // 緯度
    let lng = e.latlng.lng; // 經度

    marker = new L.marker(e.latlng, {draggable:'true'});
    marker
        .on('dragend', function(event){
            var marker = event.target;
            var position = marker.getLatLng();
            lat = position.lat;
            lng = position.lng;
            console.log(position);
            marker
                .setLatLng(position)
                .setPopupContent(`緯度：${lat}<br/>經度：${lng}`)
                .update();
        })
        .bindPopup(`緯度：${lat}<br/>經度：${lng}`)
        .on('click', onMarkerClick);
    marker.addTo(map);


}

map.on('click', onMapClick);