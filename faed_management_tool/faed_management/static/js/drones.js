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
  setAllMap(map);
}


// Add a marker to the map and push to the array.
function addMarker(location, map, image) {
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    icon: image
  });
  markers.push(marker);

}



function loadHangars(){

var hangar = {}

// First, create an object containing LatLng and radius for each city.
hangar['Cappont'] = {
  center: new google.maps.LatLng(41.608893, 0.624216),
  radius: 30
};
hangar['La Bordeta'] = {
  center: new google.maps.LatLng(41.602848,  0.640035),
  radius: 25
};
hangar['Balafia'] = {
  center: new google.maps.LatLng(41.630424, 0.627139),
  radius: 40
};
hangar['Pardinyes'] = {
  center: new google.maps.LatLng(41.623816, 0.636538),
  radius: 50
};
hangar['Templers'] = {
  center: new google.maps.LatLng(41.610229, 0.608600),
  radius: 30
};
hangar['Centre històric'] = {
  center: new google.maps.LatLng(41.617147, 0.624870),
  radius: 30
};

return hangar;
}


function loadDroppoints(){

var droppoint = {}

droppoint['droppoint1'] = {
  center: new google.maps.LatLng(41.59852869275755, 0.6444969447127424),
};
droppoint['droppoint2'] = {
  center: new google.maps.LatLng(41.60410285098816, 0.6425707137480297),
};
droppoint['droppoint3'] = {
  center: new google.maps.LatLng(41.60418590491803, 0.646008913965721),
};
droppoint['droppoint4'] = {
  center: new google.maps.LatLng(41.60079657126098, 0.6427229345719954),
};

return droppoint
}

