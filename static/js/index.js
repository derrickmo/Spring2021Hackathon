let map, heatmap;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: { lat: 37.7839, lng: -122.444 },
        mapTypeId: "roadmap",
    });
    autoComplete();
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map,
    });
    heatmap.set("radius", heatmap.get("radius") ? null : 20);

}

function toggleHeatmap() {
    heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
    const gradient = [
        "rgba(0, 255, 255, 0)",
        "rgba(0, 255, 255, 1)",
        "rgba(0, 191, 255, 1)",
        "rgba(0, 127, 255, 1)",
        "rgba(0, 63, 255, 1)",
        "rgba(0, 0, 255, 1)",
        "rgba(0, 0, 223, 1)",
        "rgba(0, 0, 191, 1)",
        "rgba(0, 0, 159, 1)",
        "rgba(0, 0, 127, 1)",
        "rgba(63, 0, 91, 1)",
        "rgba(127, 0, 63, 1)",
        "rgba(191, 0, 31, 1)",
        "rgba(255, 0, 0, 1)",
    ];
    heatmap.set("gradient", heatmap.get("gradient") ? null : gradient);
}

function changeRadius() {
    heatmap.set("radius", heatmap.get("radius") ? null : 20);
}

function changeOpacity() {
    heatmap.set("opacity", heatmap.get("opacity") ? null : 0.2);
}

// Heatmap data: 500 Points
// window.response = {
//     "37.782551, -122.445368":10,
//     "37.782745, -122.444586":21,
//     "37.782842, -122.42688":30,
//     "37.782919, -122.442815":33,
//     "37.782992, -122.442112":40,
//     "37.7831, -122.441461":50,
//     "37.783206, -122.440829":60,
//     "37.783273, -122.440324":75,
//     "37.783316, -122.440023":80,
//     "37.783357, -122.439794":91,
//     "37.783371, -122.439687":95,
//     "37.783368, -122.439666":99,
//     "37.783383, -122.439594":100,
// }

function getPoints() {
    var icon = {
        //url: "static/css/Images/icon.png", // url
        size: new google.maps.Size(15,15),
        origin: new google.maps.Point(0,0), // origin
        anchor: new google.maps.Point(0, 0), // anchor
    };
    var scores = window.response;
    let heappoints = [];
    let v_limit_min = 180;
    let v_limit_max = -180;
    let h_limit_min = 180;
    let h_limit_max = -180;
    for (x in window.response){
        let location = x.split(",");
        let ltt = Number(location[0]);
        h_limit_min = Math.min(h_limit_min, ltt);
        h_limit_max = Math.max(h_limit_max, ltt);
        let ltt_icon = Number(location[0]) + 0.000001;
        let lgt = Number(location[1]);
        v_limit_min = Math.min(v_limit_min, lgt);
        v_limit_max = Math.max(v_limit_max, lgt);
        let lgt_icon = Number(location[1]) + 0.000001;
        let marker = new google.maps.Marker({
            position:  { lat: ltt_icon, lng: lgt_icon},
            map,
            // icon: icon,
            title: window.response[x].toString(),
        });
        marker.addListener("click", () => {
            map.setZoom(20);
            map.setCenter(marker.getPosition());
        });
        map.setCenter({lat: (h_limit_min + h_limit_max)* 0.5, lng: (v_limit_min + v_limit_max) * 0.5});
        heappoints.push({location: new google.maps.LatLng(ltt,lgt), weight: window.response[x]});
    }


    return heappoints;
}

function autoComplete (){
  const input = document.getElementById("input");
  const autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.setFields(["address_components", "geometry", "icon", "name"]);
  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    console.log(place.name)
    console.log(place.geometry)
    // if (!place.geometry) {
    //   window.alert("No details available for input: '" + place.name + "'");
    //   return;
    // }
  });

}
function updateSlider(type1) {
        let sliderDiv = document.getElementById("type1");
        sliderDiv.innerHTML = type1;
    }
    function updateSlider1(type2) {
        let sliderDiv = document.getElementById("type2");
        sliderDiv.innerHTML = type2;
    }
    function updateSlider2(type3) {
        let sliderDiv = document.getElementById("type3");
        sliderDiv.innerHTML = type3;
    }