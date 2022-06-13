
const center = [23.85260389794438, 119.6];



const map = L.map('map', {
    center: center, // 中心點座標
    zoom: 8, // 0 - 18
    attributionControl: true, // 是否秀出「leaflet」的貢獻標記
    zoomControl: true , // 是否秀出 - + 按鈕
    renderer: L.canvas()
})

L.tileLayer('http://localhost:3650/api/maps/map/{z}/{x}/{y}.png', {
    maxZoom: 15,
    minZoom: 4,
    id: 'TaiwanEMap',
}).addTo(map);

