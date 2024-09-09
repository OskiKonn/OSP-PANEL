
<?php

    // Connection parameters
    require_once("connect.php");
    $connection = connect();

    if (!$connection) {
        die("Error: Could not connect to a database" . pg_last_error());
    }

    $login = $_POST["login"];
    $password = $_POST["password"];

    $query = "SELECT password, permissions FROM users WHERE login=$1";
    $result = pg_query_params($connection, $query, array($login));

    if (!$result) {
        die(json_encode(array('status' => 'denied', 'msg' => 'Cannot fetch data')));
    }

    $user = pg_fetch_assoc($result);

    if ($user && $user['password'] == $password){
        $response = array(
            'status' => 'approved',
            'permissions' => $user['permissions'],
            'msg' => 'succesful login'
        );
        echo json_encode($response);
    } else {
        $response = array(
            'status' => 'denied',
            'msg' => 'login failed'
        );
        echo json_encode($response);
    }

    $con_close = pg_close($connection);

?>
