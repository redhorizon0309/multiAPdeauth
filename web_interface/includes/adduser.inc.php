<?php 

if (isset($_POST["submit"])) {
    $name = $_POST["name"];
    $pwd = $_POST["password"];
    $pwdRepeat = $_POST["passwordPepeat"];

    require_once "dbh.inc.php";
    require_once "func.inc.php";

    if (empty_input_signup($name, $pwd, $pwdRepeat) == true) {
        header("location: ../adduser.php?error=emptyinput");
        exit();
    }
    if (invalid_name($name) == true) {
        header("location: ../adduser.php?error=invalidname");
        exit();
    }
    if (mismatch_pass($pwd,$pwdRepeat) == true) {
        header("location: ../adduser.php?error=pwdmismatch");
        exit();
    }
    if (invalid_pass($pwd,$pwdRepeat) == true) {
        header("location: ../adduser.php?error=invalidpass");
        exit();
    }
    if (name_exist($conn, $name) == true) {
        header("location: ../adduser.php?error=namexisted");
        exit();
    }

    create_user($conn, $name, $pwd);
}
else {
    header("location: ../adduser.php");
}
