let map, heatmap;

function initMap() {
  autoComplete();
  map = new google.maps.Map(
      document.getElementById("map"), {
        zoom: 11,
        center: { lat: 37.7839, lng: -122.444 },
        mapTypeId: "roadmap",
  });
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
          map.setZoom(13);
          map.setCenter(marker.getPosition());
        });
        map.setCenter({lat: (h_limit_min + h_limit_max)* 0.5, lng: (v_limit_min + v_limit_max) * 0.5});
        heappoints.push({location: new google.maps.LatLng(ltt,lgt), weight: (10 * window.response[x] - 80)});
    }


  return heappoints;
}
