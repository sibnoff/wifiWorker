function onAjaxSuccessHostapd(data)
{
    $("#table_clients").html(data);
}
function hostapdGetLogs()
{
    $.ajax({url: "/hostapd-get-logs/",
    type: "GET",
    cache: false,
    success: onAjaxSuccessHostapd});
}

function startAP() {
    $.ajax({url: "/start-hotspot/",
            type: "POST",
            cache: false,
            data: "host_iface=" + $('input[name=host_iface]:checked').val() +
                  "&gate_iface=" + $('input[name=gate_iface]:checked').val() +
                  "&hs_essid=" + $('#hs_essid').val() +
                  "&hs_security=" + $('input[name=hs_security]:checked').val() +
                  "&hs_psk=" + $('#hs_psk').val(),
            success: function (html){$("#ap_status").html(html);}});
}
function stopAP()
{
    $.ajax({url: "/stop-hotspot/",
    type: "GET",
    cache: false,
    success: function (html){$("#ap_status").html(html);}});
}


setInterval(hostapdGetLogs, 1000);
$('#hs_start').on('click', startAP)
$('#hs_stop').on('click', stopAP)
