// Management of the end of the loading of the web page
window.addEventListener("load", function () {
  var boutonElt = document.getElementById("search");
  
  // Adding a manager for the click event
  boutonElt.addEventListener("click", function () {
    var form = document.querySelector("form");

    // Displays all data entered or selected
    form.addEventListener("submit", function (e) {
      var query = form.elements.query.value;
      query = query.replace(/\s/g,'');
      if (query == "") {
        alert("Question must be filled out");
        e.preventDefault(); // Cancel sending data
        return false;
      }
      e.preventDefault(); // Cancel sending data
      // Make an AJAX GET call
      // Takes into parameters the target URL and callback function if success
      function ajaxGet(url, callback) {
        var req = new XMLHttpRequest();
        req.open("GET", url);
        req.addEventListener("load", function () {
          if (req.status >= 200 && req.status < 400) {
              callback(req.responseText);
          } 
          else {
              console.error(req.status + " " + req.statusText + " " + url);
          }
        });
        req.addEventListener("error", function () {
            console.error("Erreur réseau avec l'URL " + url);
        });
        req.send(null);
      }

      function display(reponse) {
        console.log(reponse)
        var obj = JSON.parse(reponse);

        if (obj.status==="ZERO_RESULTS") {
          // array empty or does not exist
          window.alert("Any results!! Try again.");
        }
        // Get coordinates from json
        var latitude = obj.results[0].geometry.location.lat
        var longitude = obj.results[0].geometry.location.lng
        var address = obj.results[0].formatted_address
        // Prepaire data to display
        var data = { 
          "latitude": latitude, 
          "longitude": longitude,
          "address" : address
        };
        // display message
        $.ajax({
          url: "/get_word",
          type: "POST",
          data: JSON.stringify(data),
          contentType: "application/json",
          dataType: "json",
      
          success: function (response) { 
            $("#message").html(response.html);
          }, 
          error: function () { 
            console.log("erreur summary"+xhr) 
          }
        });
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
      }
      ajaxGet("https://maps.googleapis.com/maps/api/geocode/json?key=API_KEY&address="+query, display);
    }); 
  });
});