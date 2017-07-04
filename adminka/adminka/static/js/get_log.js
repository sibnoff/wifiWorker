function onAjaxSuccess(data)
{
    $("#logs").html(data);
}
function getLogs()
{
    $.ajax({url: "/get-logs/",
    type: "GET",
    cache: false,
    data: "count_rows=30" + "&file_name=main.log",
    success: onAjaxSuccess});
}
setInterval(getLogs, 2000);