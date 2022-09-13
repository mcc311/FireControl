const center = [23.85260389794438, 119.6];
window.sessionStorage.clear();
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
    zoom: 8, // 0 - 14
    attributionControl: true, // 是否秀出「leaflet」的貢獻標記
    zoomControl: true , // 是否秀出 - + 按鈕
}).on('click', onMapClick);


L.tileLayer(/*'http://localhost:3650/api/maps/map/{z}/{x}/{y}.png'*/ "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 15,
    minZoom: 4,
    id: 'TaiwanEMap',
}).addTo(map);

function onMarkerClick(){
    const id = this.options.id;
    let $form = document.getElementById(`ship-form-${id}`);
    for(let i = 0; i < $form.length; i++){
        $form[i].value = window.sessionStorage.getItem($form[i].id);
    }

}

let adding_enemy = true; // 預設為「新增敵人」
function AddingEnemyMarker(){
    adding_enemy = true;
}
function AddingAllyMarker(){
    adding_enemy = false;
}

class MarkerInfo {
    constructor(id, is_enemy, lat, lng, typename= is_enemy? Enemy[0].typename:Ally[0].typename, type_id= is_enemy? Enemy[0].type_id:Ally[0].type_id, weapon1_id=0, weapon2_id=0) {
        this.id = id;
        this.typename = typename;
        this.type_id = type_id;
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
    const enemyIcon = L.divIcon({
        html: `
            <svg
            width="40"
            height="40"
            viewBox="0 0 30 30"
            version="1.1"
            preserveAspectRatio="none"
            >
            <path d="M20 21c-1.39 0-2.78-.47-4-1.32-2.44 1.71-5.56 1.71-8 0C6.78 20.53 5.39 21 4 21H2v2h2c1.38 0 2.74-.35 4-.99 2.52 1.29 5.48 1.29 8 0 1.26.65 2.62.99 4 .99h2v-2h-2zM3.95 19H4c1.6 0 3.02-.88 4-2 .98 1.12 2.4 2 4 2s3.02-.88 4-2c.98 1.12 2.4 2 4 2h.05l1.89-6.68c.08-.26.06-.54-.06-.78s-.34-.42-.6-.5L20 10.62V6c0-1.1-.9-2-2-2h-3V1H9v3H6c-1.1 0-2 .9-2 2v4.62l-1.29.42c-.26.08-.48.26-.6.5s-.15.52-.06.78L3.95 19zM6 6h12v3.97L12 8 6 9.97V6z";
            fill="#f2022e"></path>
            </svg>`,
        className: "",
        iconSize: [30, 30],
        iconAnchor: [15, 25],
        });
        const allyIcon = L.divIcon({
        html: `
            <svg
            width="40"
            height="40"
            viewBox="0 0 30 30"
            version="1.1"
            preserveAspectRatio="none"
            >
            <path d="M20 21c-1.39 0-2.78-.47-4-1.32-2.44 1.71-5.56 1.71-8 0C6.78 20.53 5.39 21 4 21H2v2h2c1.38 0 2.74-.35 4-.99 2.52 1.29 5.48 1.29 8 0 1.26.65 2.62.99 4 .99h2v-2h-2zM3.95 19H4c1.6 0 3.02-.88 4-2 .98 1.12 2.4 2 4 2s3.02-.88 4-2c.98 1.12 2.4 2 4 2h.05l1.89-6.68c.08-.26.06-.54-.06-.78s-.34-.42-.6-.5L20 10.62V6c0-1.1-.9-2-2-2h-3V1H9v3H6c-1.1 0-2 .9-2 2v4.62l-1.29.42c-.26.08-.48.26-.6.5s-.15.52-.06.78L3.95 19zM6 6h12v3.97L12 8 6 9.97V6z";
            fill="#0576e8"></path>
            </svg>`,
        className: "",
        iconSize: [30, 30],
        iconAnchor: [15, 25],
        });

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
                .bindPopup(`${shipForm(new_marker.options.id, new_marker.options.is_enemy, new_marker.getLatLng())}<br/>緯度：${lat}<br/>經度：${lng}`, {maxWidth:'auto', id: new_marker.options.id})
                .setLatLng(position)
                .update();
        })
        .bindTooltip(()=>{
            const info = markers_info[new_marker.options.id];
            return `(${info.id}) ${info.typename} ${info.type_id}`;
        }, {
        direction: 'bottom', // right、left、top、bottom、center。default: auto
        sticky: false, // true 跟著滑鼠移動。default: false
        permanent: false, // 是滑鼠移過才出現，還是一直出現
        opacity: 1.0
        })
        .bindPopup(`${shipForm(new_marker.options.id, new_marker.options.is_enemy,   new_marker.getLatLng())}<br/>緯度：${lat}<br/>經度：${lng}`,
            {maxWidth:'auto', id: new_marker.options.id})
        .on('click', onMarkerClick)
        .addTo(map);

    markers_info[new_marker.options.id] = new MarkerInfo(new_marker.options.id, adding_enemy, lat, lng);

    new_marker.openPopup();
    new_marker
        .getPopup().on('remove', function(event){
            const id = event.target.options.id;
            const marker = map.getMarkerById(id);
            let $form = document.getElementById(`ship-form-${id}`);
            for(let i = 0; i < $form.length; i++){
                window.sessionStorage.setItem($form[i].id, $form[i].value);
            }
            let info = markers_info[new_marker.options.id];
            let new_ship = Vessel[$form[0].value];
            info.typename = new_ship.typename;
            info.type_id = new_ship.type_id;
            // const lat = $form[`ship-form-${id}`+'_lat'].value;
            // const lng = $form[`ship-form-${id}`+'_lng'].value;
            // event.target
            //     .setLatLng([lat, lng])
            //     .update();
        })
}


const shipForm = (id, is_enemy, pos) =>{

    const VesselToHTMLSelect = (options, select_id, label)=>{
        let $div = $('<div>');
        $div.append($('<label>'), label);
        let hirachic_ship = {}
        let $select = $("<select>", {id:select_id});
        options.forEach((opt)=>{
            if (hirachic_ship[opt.typename] === undefined)
                hirachic_ship[opt.typename] = [[opt.id, opt.type_id]];
            else
                hirachic_ship[opt.typename].push([opt.id, opt.type_id])
        });
        for (const [typename, ships] of Object.entries(hirachic_ship)) {
            let $optgroup = $("<optgroup>", {label: typename});
            $optgroup.appendTo($select);
            for (const [id, type_id] of ships) {
                let $option = $("<option>", {text: type_id, value: id});
                $option.appendTo($optgroup);
            }
        }
        // return $select;
        $select.change(function(){
            alert(123);
        })
        return $div.append($('<div>').append($select));
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
        return $div.append($('<div>').append($select).append($("<div>荷彈量</div>").append($("<input>", {type:"number", value:2, step:1, id:`${select_id}_num`}))));
    }


    let $form = $(`<form id="ship-form-${id}" class='form-check-inline'></form>`);
    $form.append($(`<span value={is_enemy ? "敵方" : "我方"}>`))
    if(is_enemy){
        $form.append(VesselToHTMLSelect(Enemy, `ship-form-${id}_enemy`, '艦型'));
        $form.append(MissileToHTMLSelect(EnemyWeapon, `ship-form-${id}_weapon1`, '最大火力'));
    }else{
        $form.append(VesselToHTMLSelect(Ally, `ship-form-${id}_ally`, '我軍艦型'));
        $form.append(MissileToHTMLSelect(AllyWeapon, `ship-form-${id}_weapon1`, '火力1'));
        $form.append(MissileToHTMLSelect(AllyWeapon, `ship-form-${id}_weapon2`, '火力2'));
    }

    const lat = pos.lat;
    const lng = pos.lng;

    return $('<div>').append($form).html();
}

const EnemyWeapon = []
const AllyWeapon = []
$.getJSON('/api/missile/',function( data ) {
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
const Vessel = {};
$.getJSON('/api/vessel/',function( data ) {
    $.each( data, function( key, val ) {
        Vessel[val.id]=val;
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
