function monitoringGetLogs()
{
    $.ajax({url: "/monitoring-get-logs/",
    type: "GET",
    cache: false,
    success: function (data) {$("#monitor_tables").html(data);}});
}

function startMonitor()
{
    $.ajax({url: "/start-monitor/",
            type: "POST",
            cache: false,
            data: "mon_iface=" + $('input[name=mon_iface]:checked').val(),
            success: function (html){$("#monitor_status").html(html);}});
}
function stopMonitor()
{
    $.ajax({url: "/stop-monitor/",
    type: "GET",
    cache: false,
    success: function (html){$("#monitor_status").html(html);}});
}


setInterval(monitoringGetLogs, 5000);
$('#mon_start').on('click', startMonitor);
$('#mon_stop').on('click', stopMonitor);