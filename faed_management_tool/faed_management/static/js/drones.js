// Sets the map on all markers in the array.
function setAllMap(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setAllMap(null);
}

// Shows any markers currently in the array.
function showMarkers() {
console.log(map);
  setAllMap(map);
}

function addCircle(location, map, title, radius){

 var radiusOptions = {
      strokeColor: '#4F35DA',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#88AFEA',
      fillOpacity: 0.5,
      map: map,
      title: title,
      center: location,
      radius: Math.sqrt(radius) * 100
    };
    // Add the circle for this city to the map.
    cityCircle = new google.maps.Circle(radiusOptions);
    circles.push(cityCircle)
}


// Add a marker to the map and push to the array.
function addMarkerIcon(location, map, image,title) {
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: title,
    icon: image
  });
  markers.push(marker);
}

// Add a marker to the map and push to the array.
function addMarker(location, map,title) {
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: title,
  });
  markers.push(marker);
}



function loadHangars(){

var hangar = {}

var url = "http://localhost:8000/api/hangars/?format=json";

$.getJSON( url, function( data ) {
  var items = [];
  $.each( data, function( key, val ) {

    if (key == "results"){
      var results = val;
    $.each( results, function (key,val){
        hangar[val.id] = {
  center: new google.maps.LatLng(val.latitude, val.longitude),
  radius: val.radius,
  title:"hangar"
};

    })
    }
  });

});
return hangar;
}


function loadDroppoints(){

var droppoint = {}

var url = "http://localhost:8000/api/droppoints/?format=json";

$.getJSON( url, function( data ) {
  var items = [];
  $.each( data, function( key, val ) {

    if (key == "results"){
      var results = val;

    $.each( results, function (key,val){
        console.log(val)
        droppoint[val.name] = {
  center: new google.maps.LatLng(val.latitude, val.longitude),
  title:"droppoint"
};

    })
    }
  });

});
return droppoint


}

function weatherStation(){


}

