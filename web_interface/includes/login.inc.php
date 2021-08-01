<?php 

if (isset($_POST["submit"])) {
    $name = $_POST["name"];
    $pwd = $_POST["password"];
    $pwdRepeat = $_POST["passwordPepeat"];

    require_once "dbh.inc.php";
    require_once "func.inc.php";

    if (empty_input_login($name, $pwd) == true) {
        header("location: ../login.php?error=emptyinput");
        exit();
    }

    login_user($conn, $name, $pwd);

}
else {
    header("location: ../login.php");
}
