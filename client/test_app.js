// source code header

// initialize
function initialize(){
    console.log("initialize.");
}

$(document).ready(() => {
    initialize();

    // leaflet
    var map = L.map('map').setView([35.65, 139.7], 15);


    // Leaflet.draw test
    let editableLayers = new L.FeatureGroup();
    map.addLayer(editableLayers);

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
    // Stamen Terrain
    const stamen_terrain = L.tileLayer('http://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.png',
        {attribution: '<a id="home-link" target="_top" href="http://maps.stamen.com/">Map tiles</a> by <a target="_top" href="http://stamen.com">Stamen Design</a>, under <a target="_top" href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data © <a target="_top" href="http://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>.'});
    const stamen_toner = L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',
        {attribution: '<a id="home-link" target="_top" href="../">Map tiles</a> by <a target="_top" href="http://stamen.com">Stamen Design</a>, under <a target="_top" href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a target="_top" href="http://openstreetmap.org">OpenStreetMap</a>, under <a target="_top" href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.'});
    const stamen_watercolor = L.tileLayer('http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png',
        {attribution: 'Map tiles by <a href="https://stamen.com/" target="_blank">Stamen Design</a>, under <a href="https://creativecommons.org/licenses/by/3.0/" target="_blank">CC BY 3.0</a>. © <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors.'});
    const arcgis_world_imaginary = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'});
    //オープンストリートマップのタイル
    const osm = L.tileLayer('http://tile.openstreetmap.jp/{z}/{x}/{y}.png',
        {  attribution: "<a href='http://osm.org/copyright' target='_blank'>OpenStreetMap</a> contributors" });
    //baseMapsオブジェクトのプロパティに3つのタイルを設定
    const baseMaps = {
        "地理院地図" : gsi,
        "淡色地図" : gsipale,
        "Stamen Terrain": stamen_terrain,
        "Stamen Toner": stamen_toner,
        "Stamen WaterColor": stamen_watercolor,
        "World Imaginary": arcgis_world_imaginary,
        "OpenStreetMap" : osm.addTo(map),  // 1つだけaddToしておくとデフォルト表示になる
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

    // Leaflet.draw test
    // let editableLayers = new L.FeatureGroup();
    // map.addLayer(editableLayers);

    var options = {
        position: 'topleft',
        draw: {
            polyline: {
                shapeOptions: {
                    color: '#f357a1',
                    weight: 3
                }
            },
            polygon: {
                allowIntersection: false, // Restricts shapes to simple polygons
                drawError: {
                    color: '#e1e100', // Color the shape will turn when intersects
                    message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
                },
                shapeOptions: {
                    color: '#bada55'
                }
            },
            circle: false, // Turns off this drawing tool
            rectangle: {
                shapeOptions: {
                    clickable: false
                }
            },
            // marker: {
            //     icon: new MyCustomMarker()
            // }
        },
        edit: {
            featureGroup: editableLayers, //REQUIRED!!
            remove: false
        }
    };

    var drawControl = new L.Control.Draw(options);
    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, function (e) {
        var type = e.layerType,
            layer = e.layer;

        // if (type === 'marker') {
        //     layer.bindPopup('A popup!');
        // }

        editableLayers.addLayer(layer);
    });

});
