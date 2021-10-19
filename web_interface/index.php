<?php
	include_once 'header.php';
?>
<?php
	if (isset($_SESSION["name"])){
		echo "<p>Welcome</p>".$_SESSION["name"];
	}
	else {
		echo "<p>Login first</p>";
	}
?>		
<?php
	include_once 'footer.php';
?>