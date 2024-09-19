<?php

    require_once("connect.php");

    $connection = connect();

    $section = $_POST['section'];
    $updates = array();
    $values = array();
    $i = 1;

    foreach ($_POST as $key => $value){
        if ($key !== 'id' && $key !== 'section') {      // If key doesn't contain id
            $updates[] = "$key = \$$i";
            if ($value === 'NULL') {
                $values[] = NULL;
            } else{
                $values[] = $value;
            }
            $i++;
        }
    }

    $values[] = $_POST['id'];     // Assigning id to the last parameter

    switch ($section) {
        case 'wyjazdy':
            $query = "UPDATE wyjazdy SET " . implode(", ", $updates) . " WHERE wyjazd_id = \$$i";
            $update_columns = pg_query_params($connection, $query, $values);

        if (!$update_columns) {
            die("Update failed: " . pg_last_error());
        }

        echo "Query successful";
    }

    pg_close($connection);
?>