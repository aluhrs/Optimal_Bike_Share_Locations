//TODO: update javascript getElementById with jquery 

var map;
function initialize() {

  $("#legend").css({"display":"block"});
  $("#intro").css({"display":"block"});

  // set the zoom level and where to center the map
  var mapOptions = {
    center: new google.maps.LatLng(37.7792149, -122.4414891),
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

  // wrap this whole thing in a function similar
  // to how I did place the hot spots
  var currStationList = []
  $.ajax({
    url: "/ajax/currentstations",
    dataType: "json"          
  }).done(function(stations) {
    var lat, lng;
    for (var i=0; i<stations.length; i++) {
      lat = stations[i]["latitude"];
      lng = stations[i]["longitude"];
      if (stations[i]["city"] == "San Francisco") {
        // place the lat, longs on the map        
        marker = new google.maps.Marker({
          position: new google.maps.LatLng(lat,lng),
          map: map,
          title: stations[i]["stationName"]
            //icon: image
        });
      }
    }
    
  });


  placePossibleStations(image);
  
  map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
  map.controls[google.maps.ControlPosition.RIGHT_TOP].push(intro);

}

// Removes the Markers from the map
function clearMarkers(list) {
  console.log("this should be displaying twice.");
  placeMarker(list, null);
}

function placeMarker(list, theMap){
  for (var i=0; i<list.length; i++){
    list[i].setMap(theMap);
  }
}

var possibleStationsList = [];
function placePossibleStations(image){
  // jquery and ajax to loop through the list of hot spots
  // and place the lat/longs on the map
  if (possibleStationsList.length !== 0){
    placeMarker(possibleStationsList, map);
  } else {
    $.ajax({
      url: "/ajax/possiblestations",
      dataType: "json"          
    }).done(function(hotspots){
      var lat, lng;

      for (var i=0; i<hotspots.length; i++) {
        lat = hotspots[i]["latitude"];
        lng = hotspots[i]["longitude"];
        possibleStationsList.push(new google.maps.Marker({
          position: new google.maps.LatLng(lat,lng),
          map: map,
          title: "Possible Hot Spot",
          icon: image
        }));
      }
      placeMarker(possibleStationsList, map);     
    });
  }
}

var legend;
var intro;

var newPossibleStationsList = [];

$(document).ready(function(){
  // cache the legend before the map wipes it from the DOM
  legend = document.getElementById("legend");
  intro = document.getElementById("intro");

  $("#elevation").click(function(){
    if($("#elevation").is(":checked")){
      clearMarkers(possibleStationsList);
      $.ajax({
        url: "/ajax/elevation",
        // data: {}
        dataType: "json"
      }).done(function(hotspots){
        var lat, lng;
        var image = 'http://www.placekitten.com/32/32'; 
        for (var i=0; i<hotspots.length; i++){
          lat = hotspots[i]["latitude"];
          lng = hotspots[i]["longitude"];
          newPossibleStationsList.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "Possible Hot Spot",
            icon: image
          }));
        placeMarker(newPossibleStationsList, map); 
      }
      })
    }
    else {
      clearMarkers(newPossibleStationsList);
      placeMarker(possibleStationsList, map);
    }
  });
  

  // load the map
  google.maps.event.addDomListener(window, 'load', initialize);
})