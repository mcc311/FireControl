const center = [24.998357333095207, 121.57946295231254];
const map = L.map('map', {
    center: center, // 中心點座標
    zoom: 15, // 0 - 18
    attributionControl: true, // 是否秀出「leaflet」的貢獻標記
    zoomControl: true , // 是否秀出 - + 按鈕
}).on('click', onMapClick);

// load the map-tile file
const mb = L.tileLayer.mbTiles("./TaiwanEMap.mbtiles")
    .on('databaseloaded', function(ev) {
    console.info('MBTiles DB loaded', ev);
    })
    .on('databaseerror', function(ev) {
    console.info('MBTiles DB error', ev);
    })
    .addTo(map);

markers_info = []

function onMarkerClick(){
    this.openPopup();
}

function onMapClick(e) {
    let lat = e.latlng.lat; // 緯度
    let lng = e.latlng.lng; // 經度

    marker = new L.marker(e.latlng, {draggable:'true', id: markers_info.length+1});
    marker
        .on('dragend', function(event){
            const marker = event.target;
            const position = marker.getLatLng();
            lat = position.lat;
            lng = position.lng;
            console.log(position);
            marker
                .setLatLng(position)
                .setPopupContent(`緯度：${lat}<br/>經度：${lng}`)
                .update();
        })
        .bindPopup(`${shipForm(marker.options.id)}<br/>緯度：${lat}<br/>經度：${lng}`)
        .on('click', onMarkerClick)
        .addTo(map);
    markers_info.push(marker.options.id);
}

const shipForm = (id) =>{
    let $form = $(`<form id="ship form-${id}"></form>`);
    $form.append(toHTMLSelect(Enemy, "ship form-${id} enemy"));
    $form.append(toHTMLSelect(EnemyWeapon, "ship form-${id} enemy-weapon"));
    $form.append(toHTMLSelect(Ally, "ship form-${id} ally"));
    $form.append(toHTMLSelect(AllyWeapon, "ship form-${id} ally-weapon"));

    return $('<div>').append($form).html();
}

const toHTMLSelect = (options, select_id)=>{
    let $select = $(`<select id=${select_id}></select>`);
    options.forEach((opt)=>{
        $select.append($('<option>',{
            value: opt.id,
            text: opt.type
        }));
    });
    return $select;
}

const Enemy = [
    {
        'id': '1',
        'type': 'e1'
    },{
        'id': '2',
        'type': 'e2'
    },{
        'id': '3',
        'type': 'e3'
    },
]

const EnemyWeapon = [
    {
        'id': '1',
        'type': 'ew1'
    },{
        'id': '2',
        'type': 'ew2'
    },{
        'id': '3',
        'type': 'ew3'
    },
]

const Ally = [
    {
        'id': '1',
        'type': 'a1'
    },{
        'id': '2',
        'type': 'a2'
    },{
        'id': '3',
        'type': 'a3'
    },
]

const AllyWeapon = [
    {
        'id': '1',
        'type': 'aw1'
    },{
        'id': '2',
        'type': 'aw2'
    },{
        'id': '3',
        'type': 'aw3'
    },
]