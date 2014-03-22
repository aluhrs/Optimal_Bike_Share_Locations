//TODO: update javascript getElementById with jquery 

var map;
function initialize() {

  // set the zoom level and where to center the map
  var mapOptions = {
    center: new google.maps.LatLng(37.7577, -122.4376),
    zoom: 13
  };

  // create a new map object with the options
  map = new google.maps.Map(document.getElementById("map-canvas"),
      mapOptions);

  // layer the map with the bike routes
  var bikeLayer = new google.maps.BicyclingLayer();
  bikeLayer.setMap(map);


  // jquery and ajax to loop through the list of stations
  // and place the lat/longs on the map
  // var image = '/static/images/bikesharelogo.jpeg';
  var image = 'http://www.placekitten.com/32/32'; 

  $.ajax({
    url: "/ajax/currentstations",
    dataType: "json"          
  }).done(function(stations) {
    for (var i=0; i<stations.length; i++) {
      var lat = stations[i]["latitude"];
      var lng = stations[i]["longitude"];
      if (stations[i]["city"] == "San Francisco") {
        // place the lat, longs on the map        
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: stations[i]["stationName"]
            //icon: image
        });
      }
    }
    
  });


  // jquery and ajax to loop through the list of hot spots
  // and place the lat/longs on the map
  $.ajax({
    url: "/ajax/possiblestations",
    dataType: "json"          
  }).done(function(hotspots){
    for (var i=0; i<hotspots.length; i++) {
      var lat = hotspots[i]["latitude"];
      var lng = hotspots[i]["longitude"];
      var marker = new google.maps.Marker({
          position: new google.maps.LatLng(lat,lng),
          map: map,
          title: "Possible Hot Spot",
          icon: image
      });
    }
    
  });

  map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);

}

var legend;

$(document).ready(function(){
  // cache the legend before the map wipes it from the DOM
  legend = document.getElementById("legend");
  // load the map
  google.maps.event.addDomListener(window, 'load', initialize);
})
