function getLogs(count, file_name) {
    $.ajax({url: "/get-logs/",
            type: "GET",
            cache: false,
            data: "count_rows=" + count + "&file_name=" + file_name,
            success: onAjaxSuccess
    });
    function onAjaxSuccess(data)
    {
        $("#logs").html(data);
    }
}

setTimeout(getLogs("30", "main.log"), 1000);