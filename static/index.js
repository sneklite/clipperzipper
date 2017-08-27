$(document).ready(function() {
    $(".slide-out").hide();

    $(".orange-button").click(function() {
        var child = $(this).find("div");

        if (child.css('display') == 'none') {
            child.slideDown(300);
        } else {
            child.slideUp(300);
        }
    });
    $(".orange-button div").click(function(e) {
        e.stopPropagation();
    });
});

document.getElementById("must-fill").style.display = "none";

function reload() {
console.log("reload pressed!1")
var base = "/";
var channel = document.getElementById("channel").value;
// dgg shortcut
if (channel === "dgg") {
    channel = "Destinygg";
}
var users = document.getElementById("users").value.replace(/,/g, "").replace(/\s/g, "+");
var time_unit = document.getElementById("time-unit").value;
var time_field = document.getElementById("time-period");
var time_period = time_field.options[time_field.selectedIndex].value;
var time = "";

if (time_unit === "1") {
    console.log(time_unit);
    time_period = time_period.slice(0, time_period.length - 1);
    time = "past " + time_period;
} else if (time_unit > 1) {
    time = "past " + time_unit + " " + time_period;
} else if (time_unit != "") {
    time_period = time_period.slice(0, time_period.length - 1);
    time = "past " + time_period;
}

var mentions = "0";
if (document.getElementById("yes").checked) {
    console.log(document.getElementById("yes").checked);
    mentions = "1";
}

if (channel === "" || users === "" || time === "") {
 document.getElementById("must-fill").style.display = "inline";
} else {
console.log("reload pressed!2")
var url = base + channel + "/" + users + "/" + time + "/" + mentions
// if URL base = "/", "/" causes NS_ERROR_MALFORMED_URI
location.href = url;
}
}

 function getValues() {

 var url = window.location.href;
 var url_list = url.split("/")
 console.log(url);

 if (url_list.length > 4) {
 var mentions = url_list[url_list.length-1];
 if (mentions == "1") {
    mentions = "yes";
 } else {
    mentions = "no";
 }

 document.getElementById("mentions-name").innerHTML = "<b>Mentions only: </b>" + mentions;
 var time = url_list[url_list.length-2].replace(/%20/g, " ");
 document.getElementById("time-name").innerHTML = "<b>Time: </b>" + time;
 var users = url_list[url_list.length-3].replace(/\+/g, ", ");
 document.getElementById("users-name").innerHTML = "<b>Users: </b>" + users;
 var channel = url_list[url_list.length-4];
 document.getElementById("channel-name").innerHTML = "<b>Channel: </b>" + channel;
 document.getElementById("channel").value = channel;
     } else {
     /*
     var spans = document.getElementsByClassName('info');
     for (var i = 0; i < spans.length; i++) {
        spans[i].style.display = "none";
     }
     */
     }
 }

 getValues();
