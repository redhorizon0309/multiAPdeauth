<?php
function empty_input_signup($name, $pwd, $pwd_repeat) {
    $result;
    if (empty($name) || empty($pwd) || empty($pwd_repeat)) {
        $result = true;
    }
    else {
        $result = false;
    }
}
function empty_input_login($name, $pwd) {
    $result;
    if (empty($name) || empty($pwd)) {
        $result = true;
    }
    else {
        $result = false;
    }
} 
function invalid_name($name) {
    $result;
    if (!preg_match("/^[a-zA-Z0-9]*$/", $name)) {

    } 
    else {
        $result = false;
    }
    return $result;
}

function mismatch_pass($pwd,$pwd_repeat) {
    $result;
    if ($pwd == $pwd_repeat) {
        $result = true;
    }
    else {
        $result = false;
    }
    return $result;
}

function invalid_pass($pwd) {
    $result;
    if ((strlen($pwd)>3) && (strlen($pwd)<16)) {
        $result = false;
    }
    else {
        $result = true;
    }
    return $result;
}

function name_exist($conn, $name) {
    $sql = "SELECT * FROM users WHERE name = ?;";
    $stmt = mysqli_stmt_init($conn);
    if (!mysqli_stmt_prepare($stmt,$sql)) {
        header("location: ../adduser.php?error=stmtfailed");
        exit();
    }

    mysqli_stmt_bind_param($stmt, "s", $name);
    mysqli_stmt_execute($stmt);

    $result_data = mysqli_stmt_get_result($stmt);

    if ($row = mysqli_fetch_assoc($result_data)){
        return $row;
    }
    else {
        $result = false;
        return $result;
    }
    mysqli_stmt_close($stmt);
}

function create_user($conn, $name, $pwd) {
    $sql = "INSERT INTO users (name,password) VALUES (?, ?)";
    $stmt = mysqli_stmt_init($conn);
    if (!mysqli_stmt_prepare($stmt,$sql)) {
        header("location: ../adduser.php?error=stmtfailed");
        exit();
    }

    $pwd_hashed = password_hash($pwd, PASSWORD_DEFAULT);

    mysqli_stmt_bind_param($stmt, "ss", $name, $pwd_hashed);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_close($stmt);

    header("location: ../adduser.php?error=none");
    exit();
}

function login_user($conn, $name, $pwd) {
    $user_exist = name_exist($conn, $name);
    if ($user_exist == false) {
        header("location: ../login.php?error=wronglogin");
        exit;
    }

    $pwd_hashed = $user_exist["password"];
    $check_pwd = password_verify($pwd,$pwd_hashed);

    if ($check_pwd == false) {
        header("location: ../login.php?error=wrongpassword");
        exit;
    }
    else if ($check_pwd == true) {
        session_start();
        $_SESSION["name"] = $user_exist["name"];
        header("location: ../index.php");
        exit();
    }
}

function runPy($filePath){
    if (isset($_SESSION["name"])){
        $result = shell_exec("python3 $filePath");
        echo "<p>$result</p>";
    } else {
        echo "<p>Login first</p>";
    }
}

function scan(){
    $arg = "python3 scan.py wlan0 1";
    runPy($arg);
}


function multideauth($targetFile,$interface){
    $arg ="../multideauth.py $targetFile $interface";
    runPy($arg);
}

function test(){
    $result = runPy("../APshandler.py 2 $apid");
    echo "<p>$result</p>";
}