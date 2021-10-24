<?php
require_once "func.inc.php";

function getTableArray(){
    # get aps table
    $jsonfile = file_get_contents("APs.json");
    $apsList = json_decode($jsonfile,true);
    $aps = $apsList["aps"];
    return $aps;
}
function drawTable() {
    if(isset($_SESSION["name"])){
        # draw table header
        echo "<tr>";
        echo "<th class='id'></th>";
        echo "<th class='rssi'>RSSI</th>";
        echo "<th class='ssid'>SSID</th>";
        echo "<th class='mac'>BSSID</th>";
        echo "<th class='ch'>Channel</th>";
        echo "<th class='enc'>ENC</th>";
        //echo "<th class='selectColumn'>Selected</th>";
        echo "<th class='remove'>Select</th>";
        echo "</tr>";

        $aps = getTableArray();

        $signal_strength_pos = 0;
        $ssid_pos = 1;
        $bssid_pos = 2;
        $channel_pos = 3;
        $encryption_pos = 4;
        $select_pos = 5;
        
        # draw table content
        for ($i = 0;$i<count($aps);$i++) {
            $id=$i+1;
            $ap = $aps[$i];
            $rssid = $ap[$signal_strength_pos];
            $ssid = $ap[$ssid_pos];
            $bssid = $ap[$bssid_pos];
            $channel = $ap[$channel_pos];
            $encryption = $ap[$encryption_pos];
            $selected = $ap[$select_pos];
            if($selected == true){
                $check = "checked='true'";
            } else {
                $check = "";
            }

            echo "<tr>";
            echo "<td class='id'>$id</td>";
            echo "<td class='rssi'>$rssid</td>";
            echo "<td class='ssid'>$ssid</td>";
            echo "<td class='mac'>$bssid</td>";
            echo "<td class='ch'>$channel</td>";
            echo "<td class='enc'>$encryption</td>";
            //echo "<td class='selectColumn'><label class='checkBoxContainer'><input type='checkbox' name='selected' value='id' $check/><span class='checkmark'></span></label></td>"; 
			if($selected == true){
                echo "<td class='remove'><form method='post'><button class='red' name='deselect' type='submit' value='$id'>Selected</button></form></td>";
            } else {
                echo "<td class='remove'><form method='post'><button class='green' name='select' type='submit' value='$id'>Select</button></form></td>";
            }
            echo "</tr>";
        }
        fclose($jsonfile);
    }
}

?>