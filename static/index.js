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
document.getElementById("find-name").style.display = "none";

function reload() {

    var base = "/";
    var channel = document.getElementById("channel").value;
    // dgg shortcut
    if (channel === "dgg") {
        channel = "Destinygg";
    }
    var users = document.getElementById("users").value.replace(/,\s/g, "+");
    if (/^([a-zA-Z0-9]+,\s|\w)+$/.test(document.getElementById("users").value)) {
        var users = document.getElementById("users").value.replace(/,\s/g, "+");
    } else if (document.getElementById("users").value != "") {
        document.getElementById("must-fill").innerHTML = "users not formatted correctly";
        document.getElementById("must-fill").style.display = "inline";
        return;
    }

    if (channel === "" || users === "") {
        document.getElementById("must-fill").style.display = "inline";
    } else {
    var time_unit = document.getElementById("time-unit").value;
    var time_field = document.getElementById("time-period");
    var time_period = time_field.options[time_field.selectedIndex].value;
    time_period = time_period.replace(/\(s\)/g, "s");
    var time = "";

    if (time_unit === "1") {
        time_period = time_period.slice(0, time_period.length - 1);
        time = "past " + time_period;
    } else if (time_unit > 1) {
        time = "past " + time_unit + " " + time_period;
    } else  {
        time_period = time_period.slice(0, time_period.length - 1);
        time = "past " + time_period;
    }

    var find_tokens = "";
    if (document.getElementById("find").value != "") {
        find_tokens = "/" + document.getElementById("find").value.replace(/,\s/g, "+");
        find_tokens = find_tokens.replace()
    }

    var mentions = "0";
    if (document.getElementById("yes").checked) {
        mentions = "1";
    }

    var url = base + channel + "/" + users + "/" + time +
              "/" + mentions + find_tokens;
    // Note: if URL base = "/", "/" causes NS_ERROR_MALFORMED_URI
    location.href = url;
    }
}

function getValues() {

    var url = window.location.href;
    var url_list = url.split("/")

    if (url_list.length > 4) {

        var check = url_list[url_list.length - 2];
        var n = 0;

        if (!isNaN(check) && parseInt(Number(check)) == check &&
            !isNaN(parseInt(check, 10))) {
            // 2nd to last item is an int (mentions), so find is present
            var find = url_list[url_list.length-1].replace(/\+/g, ", ").replace(/%20/g, " ");
            document.getElementById("find-name").innerHTML = "<br><b>Search terms: </b>" +find;
            document.getElementById("find-name").style.display = "inline";
            n = 1;
        }

        var get_mentions = url_list[url_list.length - n - 1];
        var mentions = "no";
        if (get_mentions == "1") {
            mentions = "yes";
            document.getElementById("yes").checked = true;
        }

        document.getElementById("mentions-name").innerHTML = "<b>Mentions only: </b>" + mentions;
        var time = url_list[url_list.length - n - 2].replace(/%20/g, " ");
        document.getElementById("time-name").innerHTML = "<b>Time: </b>" + time;
        var users = url_list[url_list.length - n - 3].replace(/\+/g, ", ").replace(/%20/g, " ");
        document.getElementById("users-name").innerHTML = "<b>Users: </b>" + users;
        var channel = url_list[url_list.length - n - 4];
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
