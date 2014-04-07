var map;
function initialize() {
  //var marker;
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

  // layer the map with the Google Maps bike routes
  var bikeLayer = new google.maps.BicyclingLayer();
  bikeLayer.setMap(map);

  // layer the map with the Google Maps tranit routes
  var transitLayer = new google.maps.TransitLayer();
  transitLayer.setMap(map);

  var cs_image = '/static/images/rsz_baybike.png'
  var top_one = '/static/images/icon.png'
  var top_ten = '/static/images/green_icon.png'
  var rest = '/static/images/gray_icon.png'
  var image = [];
  image.push(top_one, top_ten, rest);

  var currStationList = []
  $.ajax({
    url: "/ajax/currentstations",
    dataType: "json"          
  }).done(function(stations) {
    var lat, lng;
    for (var i=0; i<stations.length; i++) {
      lat = stations[i]["latitude"];
      lng = stations[i]["longitude"];
      //if (stations[i]["city"] == "San Francisco") {
        // place the lat, longs on the map        
        marker = new google.maps.Marker({
          position: new google.maps.LatLng(lat,lng),
          map: map,
          title: stations[i]["stationName"],
          icon: cs_image
          });
    }
  });

  placePossibleStations(image);
  
  map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
}

// Removes the Markers from the map
function clearMarkers(list) {
  placeMarker(list, null);
}

function attachEventListener(marker){
  google.maps.event.addListener(marker, 'click', function(){
    console.log(marker["title"] + " got clicked!");
    var message = "<b>" + "Ranked: " + marker["cluster_rank"] + "</b>" + "<p>" + "<p>" + "This spot has " + marker["cluster_length"] + " points in its cluster.";
    var infowindow = new google.maps.InfoWindow({
      content: message
    });
    infowindow.open(marker.get('map'), marker);
  });
}

function placeMarker(list, theMap){
  console.log(list.length);
  console.log(theMap);
  for (var i=0; i<list.length; i++){
    console.log(theMap);
    list[i].setMap(theMap);
    if (theMap != null){
      console.log("this should be displaying");
      attachEventListener(list[i]);
    }
  }
}

var possibleStationsList = [];
function placePossibleStations(image)
{
  // jquery and ajax to loop through the list of hot spots
  // and place the lat/longs on the map
  if (possibleStationsList.length !== 0)
  {
    placeMarker(possibleStationsList, map);
  } else {
    $.ajax({
      url: "/ajax/possiblestations",
      dataType: "json"          
    }).done(function(hotspots)
    {
      var lat, lng, message, infowindow;
      for (var i=0; i<hotspots.length; i++) 
      {
        id = hotspots[i]["id"];
        lat = hotspots[i]["latitude"];
        lng = hotspots[i]["longitude"];
        key = hotspots[i]["key"];
        cluster = hotspots[i]["cluster"];
        cluster_length = hotspots[i]["cluster_length"];
        cluster_rank = hotspots[i]["cluster_rank"];
        if (cluster_rank == 1) 
        {
          possibleStationsList.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "'" + key + "'",
            icon: image[0],
            cluster: cluster,
            cluster_length: cluster_length,
            cluster_rank: cluster_rank
            }));
        }
        else if (cluster_rank > 1 && cluster_rank < 11)
        {
          possibleStationsList.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "'" + key + "'",
            icon: image[1],
            cluster: cluster,
            cluster_length: cluster_length,
            cluster_rank: cluster_rank
            }));
        }
        else 
        {
          possibleStationsList.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "'" + key + "'",
            icon: image[2],
            cluster: cluster,
            cluster_length: cluster_length,
            cluster_rank: cluster_rank
            }));
        }
      }
      placeMarker(possibleStationsList, map);     
    });
  }
}


var legend;

var newPossibleStationsList = [];
$(document).ready(function(){
  // cache the legend before the map wipes it from the DOM
  legend = document.getElementById("legend");
  $(".checkboxes input").click(function() {
    if($(".checkboxes input:checked").length) {
      var inputList = []
      for (var i=0; i<$(".checkboxes input:checked").length; i++) {
        inputList.push($(".checkboxes input:checked")[i]["value"]);
      }
      clearMarkers(possibleStationsList);
      $.ajax({
        url: "/ajax/legend",
        type: "GET",
        data: {"li": inputList},
        dataType: "json",
        contentType: "application/json"
      }).done(function(hotspots) {
        var lat, lng, cluster, cluster_length, cluster_rank;
        var top_one = '/static/images/icon.png'
        var top_ten = '/static/images/green_icon.png'
        var rest = '/static/images/gray_icon.png'
        clearMarkers(newPossibleStationsList);
        newPossibleStationsList = []
        for (var i=0; i<hotspots.length; i++) {
          lat = hotspots[i]["latitude"];
          lng = hotspots[i]["longitude"];
          key = hotspots[i]["key"];
          cluster = hotspots[i]["cluster"];
          cluster_length = hotspots[i]["cluster_length"];
          cluster_rank = hotspots[i]["cluster_rank"];
          //console.log(lat, lng, key, cluster, cluster_length, cluster_rank)
          if (cluster_rank == 1) 
        {
          //console.log("this is the top one" + lat,lng, top_one);
          newPossibleStationsList.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "'" + key + "'",
            icon: top_one,
            cluster: cluster,
            cluster_length: cluster_length,
            cluster_rank: cluster_rank
            }));
        }
        else if (cluster_rank > 1 && cluster_rank < 11)
        {
          newPossibleStationsList.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "'" + key + "'",
            icon: top_ten,
            cluster: cluster,
            cluster_length: cluster_length,
            cluster_rank: cluster_rank
            }));
        }
        else 
        {
          newPossibleStationsList.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "'" + key + "'",
            icon: rest,
            cluster: cluster,
            cluster_length: cluster_length,
            cluster_rank: cluster_rank
            }));
        }
        }
        placeMarker(newPossibleStationsList, map);
      })
    } 
    else 
    {
      clearMarkers(newPossibleStationsList);
      placeMarker(possibleStationsList, map);
      if (newPossibleStationsList != []) 
      {
        newPossibleStationsList = []
      }
    }
  });

  var crowdSourced = [];
  $("#all_data").change(function() {
    if(this.checked) {
      $.ajax({
        url: "/ajax/allcrowdsourced",
        dataType: "json"
      }).done(function(data){
        var id, lat, lng;
        for (var i=0; i<data.length; i++) {
          id = data[i]["id"]
          lat = data[i]["latitude"]
          lng = data[i]["longitude"]
          crowdSourced.push(new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            title: "'" + id + "'"
          }));
        }
        placeMarker(crowdSourced, map);
        //console.log(crowdSourced.length); 
      })
    } else {
      clearMarkers(crowdSourced);
      crowdSourced = [];
    }
    });




  // load the map
  google.maps.event.addDomListener(window, 'load', initialize);
});