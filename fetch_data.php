
<?php

    header('Content-Type: application/json');

    // Connection parameters
    $host = "localhost";
    $database = "OSP_GRUDZIADZ";
    $user = "postgres";
    $dbpassword = "OskarKonrad2";
    $port = "5432";

    $connection = pg_connect("host=$host port=$port dbname=$database user=$user password=$dbpassword");

    if (!$connection) {
        die("Error: Could not connect to a database" . pg_last_error());
    }

    $table = $_POST['table'];
    $mode = $_POST['mode'];
    $params = [];

    function fetch_rows(&$results, &$target_array) {
        while ($row = pg_fetch_assoc($results)) {
            $target_array[] = $row;
        }
    }

    switch ($table){
        case 'wyjazdy':
            if ($mode == 'detail') {
                $id = $_POST['id'];
                $params[] = $id; // Adds target id to parameters table
                $query = "  SELECT w.title, w.number, w.type, w.adress, w.day, cc.name || ' ' || cc.surname as commander,
                                cd.name || ' ' || cd.surname as driver, c1.name || ' ' || c1.surname as ratownik1,
                                c2.name || ' ' || c2.surname as ratownik2, c3.name || ' ' || c3.surname as ratownik3,
                                c4.name || ' ' || c4.surname as ratownik4, w.alarm, w.arrival, w.departure,
                                w.comeback
                            from wyjazdy w
                                JOIN czlonkowie as cc on w.commander=cc.czlonek_id
                                LEFT JOIN czlonkowie as cd on w.driver=cd.czlonek_id
                                LEFT JOIN czlonkowie as c1 on w.ratownik1=c1.czlonek_id
                                LEFT JOIN czlonkowie as c2 on w.ratownik2=c2.czlonek_id
                                LEFT JOIN czlonkowie as c3 on w.ratownik3=c3.czlonek_id
                                LEFT JOIN czlonkowie as c4 on w.ratownik4=c4.czlonek_id
                            WHERE w.wyjazd_id=$1;";
            }
            else {
                $query = 'SELECT title as Nazwa, day as Data, type as Rodzaj, wyjazd_id as ID FROM wyjazdy;';
            }

            $result = pg_query_params($connection, $query, $params);

            if (!$result) {
                die(json_encode(array('status' => 'failed', 'msg' => 'Failed fetching data')));
            }

            $wyjazdy = array();

            fetch_rows($result, $wyjazdy);

            echo json_encode(array('status' => 'OK', 'data' => $wyjazdy));

            break;
        case 'czlonkowie':

            $query_fighters = "SELECT name || ' ' ||surname as czlonek FROM czlonkowie;";
            $get_fighters = pg_query($connection, $query_fighters);

            if (!$get_fighters) {
                die(json_encode(array('status' => 'failed', 'msg' => 'Failed trying to query czlonkowie')));
            }

            $fighters = array();

            fetch_rows($get_fighters, $fighters);

            if ($mode == 'detail') {
                $query_commanders = "SELECT name || ' ' || surname as commander_name FROM czlonkowie where is_commander;";
                $query_drivers = "SELECT name || ' ' || surname as driver_name FROM czlonkowie where is_driver;";

                $get_commanders = pg_query($connection, $query_commanders);
                $get_drivers = pg_query($connection, $query_drivers);

                if (!$get_commanders or !$get_drivers) {
                    die(json_encode(array('status' => 'failed', 'msg' => 'Failed trying to query czlonkowie')));
                }
                
                $commanders = array();
                $drivers = array();

                fetch_rows($get_commanders, $commanders);
                fetch_rows($get_drivers, $drivers);

            }

            $czlonkowie = array('czlonkowie' => $fighters, 'commander' => $commanders, 'driver' => $drivers);

            echo json_encode(array('status' => 'OK', 'data' => $czlonkowie));
            break;
        default:
            die(json_encode(array('status' => 'failed', 'msg' => 'Provided table does not match database table')));
    }


    pg_close($connection);




?>