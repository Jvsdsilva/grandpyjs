// Management of the end of the loading of the web page
window.addEventListener("load", function () {
    var boutonElt = document.getElementById("search");
    
    // Adding a manager for the click event
    boutonElt.addEventListener("click", function () {
      var form = document.querySelector("form");
      // Displays all data entered or selected
      form.addEventListener("submit", function (e) {
          var query = form.elements.query.value;
          if (query == "") {
            alert("Question must be filled out");
            return false;
        }
        e.preventDefault(); // Cancel sending data
      }); 
    });  
});