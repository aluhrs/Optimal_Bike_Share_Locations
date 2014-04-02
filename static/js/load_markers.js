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

  // var image = '/static/images/bikesharelogo.jpeg';
  // var image = 'http://www.placekitten.com/32/32'; 
  var cs_image = '/static/images/rsz_baybike.png'
  var image = '/static/images/icon.png'

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
          title: stations[i]["stationName"],
          icon: cs_image
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
  placeMarker(list, null);
}

function placeMarker(list, theMap){
  //console.log(list.length);
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
var logo;

var newPossibleStationsList = [];
$(document).ready(function(){
  // cache the legend before the map wipes it from the DOM
  legend = document.getElementById("legend");
  intro = document.getElementById("intro");
  logo = document.getElementById("logo");
  $(".checkboxes input").click(function(){
    if($(".checkboxes input:checked").length){
      var inputList = []
      for (var i=0; i<$(".checkboxes input:checked").length; i++){
        inputList.push($(".checkboxes input:checked")[i]["value"]);
      }
      console.log("this is the console.log: " + inputList);
      clearMarkers(possibleStationsList);
      //clearMarkers(newPossibleStationsList);

      $.ajax({
        url: "/ajax/legend",
        type: "GET",
        data: {"li": inputList},
        dataType: "json",
        contentType: "application/json"
      }).done(function(hotspots){
        var lat, lng;
        var image = '/static/images/icon.png';
        clearMarkers(newPossibleStationsList);
        newPossibleStationsList = []
        for (var i=0; i<hotspots.length; i++){
          lat = hotspots[i]["latitude"];
          lng = hotspots[i]["longitude"];
          id = hotspots[i]["id"];
          newPossibleStationsList.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "id",
            icon: image
          }));

        placeMarker(newPossibleStationsList, map); 
      }
      })
    }
    else {
      clearMarkers(newPossibleStationsList);
      placeMarker(possibleStationsList, map);
      if (newPossibleStationsList != []) {
        newPossibleStationsList = []
      }
    }
  });
  

  // load the map
  google.maps.event.addDomListener(window, 'load', initialize);
})