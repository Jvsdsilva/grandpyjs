// Management of the end of the loading of the web page
window.addEventListener("load", function () {
    var boutonElt = document.getElementById("search");
    
    // Adding a manager for the click event
    boutonElt.addEventListener("click", function () {
      var form = document.querySelector("form");
      // Displays all data entered or selected
      form.addEventListener("submit", function (e) {
        // display message
        var word = $('#query').val();
        word = word.replace(/\s/g,'');
        if (word == "") {
          alert("Question must be filled out");
          e.preventDefault(); // Cancel sending data
          return false;
        }
        $.ajax({
        url: "/get_word",
        type: "GET",
        data: {word: word},
        success: function(response) {
          $("#message").html(response.html);
          // display coordinates
          $.ajax({
            url: "/get_coord",
            type: "GET",
            data: {word: word},
            success: function(response) {
              
              // Loop through the results array and place a marker for each
              // set of coordinates.
              for (var x in response){
                var building = response[x]
              }
              // data treatements
              var split = building.split(",")
              var lat = split[0]
              var lng = split[1]
              var latitude = lat.replace("[", '');
              var longitude = lng.replace("]", '');
            
              // Display map and marker
              function initMap() {
                var mapDiv = document.getElementById('googleMap');
                var map = new google.maps.Map(mapDiv, {
                  zoom: 10,
                  center: new google.maps.LatLng(latitude, longitude)
                });
                var coord= {lat: parseFloat(latitude), lng: parseFloat(longitude)};
                var marker = new google.maps.Marker({
                  position: coord,
                  map:map
                });
              }
              var coord= {lat: parseFloat(latitude), lng: parseFloat(longitude)};
              var marker = new google.maps.Marker({
                  position: coord,
                  map:initMap()
              });
            },
            error: function(xhr) {
              $("#message").html("Any results!! Try again, please.");
              console.log("erreur coordinates"+ xhr) // error coordinate
            },
          }); 
        },
        error: function(err) {
          $("#message").html("Any results!! Try again, please.");
          $.ajax({
            url: "/get_coord",
            type: "GET",
            data: {word: word},
            success: function(response) {
              $("#message").html("");
            },
          
          error: function(xhr) {
            $("#message").html("");
            console.log("erreur coordinates"+ xhr) // error coordinate
          },
        });
          console.log("erreur sommaire"+err) // error summary
        }
      });
    e.preventDefault(); // Cancel sending data
    return false;
    }); 
  });
});    
