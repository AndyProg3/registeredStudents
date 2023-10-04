$(document).ready(function() {
    $("#password").keyup(function (event) {
      if (event.keyCode == 13) {
          $("#submit").click();
      }
    });
  });

function tryLogin() {
    var userName = jQuery("#username").val();
    var pw = jQuery("#password").val();

    jQuery("#password").val("");

    jQuery.ajax({
        type: "POST",
        url: "/login?action=login",
        data: {userName : userName, pw : pw},
        success:
            function(data, textstatus) {
                pw = "";
                if(data == "success") {
                    window.location.href = "/students";
                }
                else {
                    $("#results").text("Unrecognized User Name or Password");
                }
            }
    });
}