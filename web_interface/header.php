<?php
	session_start();
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=0.8, minimal-ui">
		<meta name="theme-color" content="#36393E">

		<meta name="description" content="Master Controller">
		<title>Master Controller</title>

		<link rel="stylesheet" type="text/css" href="style.css">
		<script src="js/site.js"></script>
	</head>
	<body onload="loadLang()">
	    <nav>
			<div class="wrapper">
			<a href="index.php"></a>
			<ul class="menu">
				<li><a href="index.php">Home</a></li>
				<?php
					if (isset($_SESSION["name"])){
						echo "<li><a href=\"shell.php\">Shell</a></li>";
						echo "<li><a href=\"includes/logout.inc.php\">Logout</a></li>";
					}
					else {
						echo "<li><a href=\"adduser.php\">Add User</a></li>";
						echo "<li><a href=\"login.php\">Login</a></li>";
					}
				?>				
            </ul>
			</div>
		</nav>
        
		<div class=wrapper>

