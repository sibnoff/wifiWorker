function saveSettings() {
    $.ajax({url: "/save-settings/",
            type: "POST",
            cache: false,
            data: "db_host=" + $('#db_ip').val() +
                  "&db_name=" + $('#db_name').val() +
                  "&db_user=" + $('#db_login').val() +
                  "&db_password=" + $('#db_passwd').val(),
            success: onAjaxSuccess
    });
    function onAjaxSuccess(data)
    {
        $("#settings_bd").html(data);
        alert('Настройки успешно сохранены!');
    }
}
function loadSettings() {
    $.ajax({url: "/load-settings/",
            cache: false,
            success: function (html){$("#settings_bd").html(html);
                    alert('Настройки успешно загружены!');}});
}
function testConnection() {
    $.ajax({url: "/load-settings/",
            cache: false,
            success: function (html){$("#settings_bd").html(html);}});
}

$('#save_set').on('click', saveSettings)
$('#load_set').on('click', loadSettings)
$('#test_con').on('click', testConnection)
