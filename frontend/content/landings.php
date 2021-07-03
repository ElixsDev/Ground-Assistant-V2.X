<div id="sql_conn">
    <?php
        require "../dbstart.php";
        if ($conn_out != "Status: Connected successfully") {
            echo "MySQL Error, ".$conn_out;
        }
    ?>
</div>

<div id="landings">
    <?php
        echo time()."</br>";
        $sql = "SELECT * FROM $stddate WHERE type = \"1\" ORDER BY time DESC LIMIT 20;";
        //echo $sql;
        $result = $conn->query($sql);
        $length = $result->num_rows;
        //echo " ".$length."</br>";
        if ($length > 0) {
            for($i = 1; $row = $result->fetch_assoc(); $i++) {
                //if
                $namesql = "SELECT * FROM ogn_name_db WHERE device_id = \"".$row["device_id"]."\";";
                $nameresult = $conn->query($namesql);
                $namelength = $nameresult->num_rows;
                $namerow = $nameresult->fetch_assoc();

                if ($namerow["cn"] == "") {
                    $cn = "XX";
                } else {
                    $cn = $namerow["cn"];
                }

                if ($namerow["registration"] == "") {
                    $clearname = "X-XXXX";
                } else {
                    $clearname = $namerow["registration"];
                }

                if ($namerow["aircraft_model"] == "") {
                    $aircraft = "unknown";
                } else {
                    $aircraft = $namerow["aircraft_model"];
                }

                $antidouble[i] = $row["device_id"];
                $height = $row["msl"];

                if (in_array($row["device_id"], $planes)) {
                    echo $clearname.", ".$aircraft.", ".$height."m</br>";
                }
                $planes[i] = $row["device_id"];
            }
        } else {
            $result[0] = "0 results";
        }
    ?>
</div>
