// source code header

// initialize
function initialize(){
    console.log("initialize.");
}

$(document).ready(() => {
    initialize();

    // leaflet
    var map = L.map('map').setView([35.65, 139.7], 15);

    //L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    //}).addTo(map);

    L.marker([35.66, 139.75]).addTo(map)
        .bindPopup('A pretty CSS3 popup.<br> Easily customizable.');
        //.openPopup();

    // http://ktgis.net/service/leafletlearn/index.html
    //地理院地図の標準地図タイル
    const gsi =L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
      {attribution: "<a href='https://maps.gsi.go.jp/development/ichiran.html' target='_blank'>地理院タイル</a>"});
    //地理院地図の淡色地図タイル
    const gsipale = L.tileLayer('http://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
      {attribution: "<a href='http://portal.cyberjapan.jp/help/termsofuse.html' target='_blank'>地理院タイル</a>"});
    //オープンストリートマップのタイル
    const osm = L.tileLayer('http://tile.openstreetmap.jp/{z}/{x}/{y}.png',
      {  attribution: "<a href='http://osm.org/copyright' target='_blank'>OpenStreetMap</a> contributors" });
    //baseMapsオブジェクトのプロパティに3つのタイルを設定
    const baseMaps = {
      "地理院地図" : gsi,
      "淡色地図" : gsipale,
      "OpenStreetMap" : osm.addTo(map)  // 1つだけaddToしておくとデフォルト表示になる
    };

    // var maps = Object.assign(baseMaps, mapboxMaps);

    L.control.layers(baseMaps).addTo(map);

    L.control.scale().addTo(map);

	    // event test
    var myLines = [{
        "type": "LineString",
        "coordinates": [[138, 34.5], [139, 35.5], [140, 35]]
    }, {
        "type": "LineString",
        "coordinates": [[-105, 40], [-110, 45], [-115, 55]]
    }];
    var myStyle = {
        "color": "#ff7800",
        "weight": 5,
        "opacity": 0.65
    };
    var myLines_Geo = L.geoJSON(myLines, {
        style: myStyle
    }).addTo(map);
    myLines_Geo.on('click', () => {
      console.log("LineString clicked.");
      map.setZoom(map.getZoom() - 0.25)   // TMP for DEBUG
      console.log(map.getZoom());         // TMP for DEBUG
    });


    var latlngs = [[34.5, 138.3], [35.5, 139.3], [35, 140.3]];
    var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
    polyline.on('mouseover', () => {
      console.log("mouseover");
    }).on('mouseout', () => {
      console.log("mouseout");
      console.log(map.getZoom());   // TMP for DEBUG
    });

});
