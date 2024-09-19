<?php

    require_once("connect.php");

    $connection = connect();

    $section = $_POST['section'];
    $keys = array();
    $values = array();

    foreach ($_POST as $key => $value) {
        if ($key !== 'section') {      // If key doesn't contain id
            $keys[] = $key;

            if ($value === 'NULL') {
                $values[] = NULL;
            } else {
                $values[] = $value;
            }
        }
    }
    
    $columns = implode(", ", $keys);
    $placeholders = implode(",", array_map(function($index) {
        return "$". $index;
    }, range(1, count($values))));
    
    $query = "INSERT INTO $section ($columns) VALUES ($placeholders);";
    $insertion = pg_query_params($connection, $query, $values);

    if (!$insertion) {
        die("Insert failed" . pg_last_error($connection));
    }

    echo "Query successfull";

    pg_close($connection);

?>