
const center = [24.998357333095207, 121.57946295231254];
L.Map.include({
    getMarkerById: function (id) {
        let marker = null;
        this.eachLayer(function (layer) {
            if (layer instanceof L.Marker) {
                if (layer.options.id === id) {
                    marker = layer;
                }
            }
        });
        return marker;
    }
});

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


function onMarkerClick(){
    const id = this.options.id;
    let $form = document.getElementById(`ship-form-${id}`);
    for(let i = 0; i < $form.length-2; i++){
        $form[i].value = window.sessionStorage.getItem($form[i].id);
    }
}

let adding_enemy = true; // 預設為「新增敵人」
function changeAddingMarker(){
    adding_enemy = !adding_enemy;
}

class MarkerInfo {
    constructor(id, is_enemy, lat, lng, ship_id=0, weapon1_id=0, weapon2_id=0) {
        this.id = id;
        this.is_enemy = is_enemy;
        this.lat = lat;
        this.lng = lng;
        this.weapon1_id = weapon1_id;
        this.weapon2_id = weapon2_id;

    }
}
markers_info = {}

function onMapClick(e) {
    let lat = e.latlng.lat; // 緯度
    let lng = e.latlng.lng; // 經度
    const enemyIcon = L.icon({
        iconUrl: "assets/img/map marker/blue pin.png",
        iconSize: [30, 48],
    })
    const allyIcon = L.icon({
        iconUrl: "assets/img/map marker/red pin.png",
        iconSize: [30, 48],
    })

    let new_marker = new L.marker(e.latlng,
        {
            draggable: 'true',
            id: Object.keys(markers_info).length + 1,
            icon: adding_enemy ? enemyIcon : allyIcon,
            is_enemy: adding_enemy
        });
    new_marker
        .on('dragend', function(event){
            const marker = event.target;
            const position = marker.getLatLng();
            const lat = position.lat;
            const lng = position.lng;
            marker
                .bindPopup(`${shipForm(new_marker)}<br/>緯度：${lat}<br/>經度：${lng}`, {maxWidth:'auto', id: new_marker.options.id})
                .setLatLng(position)
                .update();
        })
        // .on('click', onMarkerClick)

        .bindPopup(`${shipForm(new_marker)}<br/>緯度：${lat}<br/>經度：${lng}`, {maxWidth:'auto', id: new_marker.options.id})
        .on('click', onMarkerClick)
        .addTo(map);
    new_marker.openPopup();
    new_marker
        .getPopup().on('remove', function(event){
            const id = event.target.options.id;
            const marker = map.getMarkerById(id);

            let $form = document.getElementById(`ship-form-${id}`);
            for(let i = 0; i < $form.length; i++){
                window.sessionStorage.setItem($form[i].id, $form[i].value);
            }
            // const lat = $form[`ship-form-${id}`+'_lat'].value;
            // const lng = $form[`ship-form-${id}`+'_lng'].value;
            // event.target
            //     .setLatLng([lat, lng])
            //     .update();
        })
    markers_info[new_marker.options.id] = new MarkerInfo(new_marker.options.id, adding_enemy, lat, lng);
}


const shipForm = (marker) =>{
    const VesselToHTMLSelect = (options, select_id, label)=>{
        let $div = $('<div>');
        $div.append($('<label>'), label);
        let hirachic_ship = {}
        let $select = $(`<select id=${select_id}></select>`);
        options.forEach((opt)=>{
            if (hirachic_ship[opt.typename] === undefined)
                hirachic_ship[opt.typename] = [[opt.id, opt.type_id]];
            else
                hirachic_ship[opt.typename].push([opt.id, opt.type_id])
        });
        console.log(hirachic_ship);
        for (const [typename, ships] of Object.entries(hirachic_ship)){
            let $optgroup = $("<optgroup>", {label:typename});
            $optgroup.appendTo($select);
            for (const [id, type_id] of ships){
                let $option = $("<option>", {text: type_id, value: id});
                $option.appendTo($optgroup);
            }
        }
        // return $select;
        return $div.append($select);
    }
    const MissileToHTMLSelect = (options, select_id, label)=>{
        let $div = $('<div>');
        $div.append($('<label>'), label);
        let $select = $(`<select id=${select_id}></select>`);
        options.forEach((opt)=>{
            let $option = $("<option>", {text: opt.type, value: opt.id});
            $option.appendTo($select);
        });
        // return $select;
        return $div.append($select);
    }


    const id = marker.options.id;
    const is_enemy = marker.options.is_enemy;
    let $form = $(`<form id="ship-form-${id}" class='form-check-inline'></form>`);
    $form.append($(`<span value={is_enemy ? "敵方" : "我方"}>`))
    if(is_enemy){
        $form.append(VesselToHTMLSelect(Enemy, `ship-form-${id}_enemy`, '艦型'));
        $form.append(MissileToHTMLSelect(EnemyWeapon, `ship-form-${id}_weapon1`, '火力1'));
        $form.append(MissileToHTMLSelect(EnemyWeapon, `ship-form-${id}_weapon2`, '火力2'));
    }else{
        $form.append(VesselToHTMLSelect(Ally, `ship-form-${id}_ally`, '我軍艦型'));
        $form.append(MissileToHTMLSelect(AllyWeapon, `ship-form-${id}_weapon1`, '火力1'));
        $form.append(MissileToHTMLSelect(AllyWeapon, `ship-form-${id}_weapon2`, '火力2'));
    }

    const toHTMLInput = (defaultValue, input_id, label)=>{
        let $div = $('<div>');
        $div.append($('<label>'), label);
        let $input = $(`<input id=${input_id} type='number' step='1e-6' value=${defaultValue} width="60px">`);
        return $div.append($input);
    }

    const pos = marker.getLatLng();
    const lat = pos.lat;
    const lng = pos.lng;
    // $form.append(toHTMLInput(lat, `ship-form-${id}_lat`, '緯度'));
    // $form.append(toHTMLInput(lng, `ship-form-${id}_lng`, '經度'));

    return $('<div>').append($form).html();
}


// const Enemy = [
//     {
//         'id': '1',
//         'type': 'e1'
//     },{
//         'id': '2',
//         'type': 'e2'
//     },{
//         'id': '3',
//         'type': 'e3'
//     },
// ]
//
// const Ally = [
//     {
//         'id': '1',
//         'type': 'a1'
//     },{
//         'id': '2',
//         'type': 'a2'
//     },{
//         'id': '3',
//         'type': 'a3'
//     },
// ]


const EnemyWeapon = []
const AllyWeapon = []
$.getJSON('http://localhost:8000/api/missile/',function( data ) {
    $.each( data, function( key, val ) {
        switch(val['belongs_to']){
            case 'b': // both
                EnemyWeapon.push(val);
                AllyWeapon.push(val);
                break;
            case 'e': //enemy
                EnemyWeapon.push(val);
                break;
            case 'a': // ally
                AllyWeapon.push(val);
                break;
        }
    });
});
const Enemy = []
const Ally = []
$.getJSON('http://localhost:8000/api/vessel/',function( data ) {
    $.each( data, function( key, val ) {
        switch(val['belongs_to']){
            case 'b': // both
                Enemy.push(val);
                Ally.push(val);
                break;
            case 'e': //enemy
                Enemy.push(val);
                break;
            case 'a': // ally
                Ally.push(val);
                break;
        }
    });
});
