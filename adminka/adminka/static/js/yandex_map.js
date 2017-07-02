function hotspot_show() {
    $.ajax({url: "/hotspot-show/",
            cache: false,
             data: "bssid=" + $('#bssid').val() +
                  "&essid=" + $('#essid').val(),
            success: function (html){$("#map_section").html(html);}});
}

function client_show() {
    $.ajax({url: "/client-show/",
            cache: false,
            data: "mac_client=" + $('#mac_client').val() +
                  "&nick_client=" + $('#nick_client').val(),
            success: function (html){$("#map_section").html(html);}});
}
function show_all_hotspot() {
    $.ajax({url: "/show-all-hotspot/",
            cache: false,
            success: function (html){$("#map_section").html(html);}});
}


$('#hotspot_show').on('click', hotspot_show)
$('#client_show').on('click', client_show)
$('#show_all_hotspot').on('click', show_all_hotspot)