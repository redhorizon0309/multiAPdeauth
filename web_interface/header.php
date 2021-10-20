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
	<body>
	    <nav>
			<div class="wrapper">
			<a href="index.php"></a>
			<ul class="menu">
				<li><a href="index.php">Master Node</a></li>
				<?php
					if (isset($_SESSION["name"])){
						echo "<li><a href=\"adduser.php\">Add User</a></li>";
						echo "<li><a href=\"scan.php\">Scan</a></li>";
						echo "<li><a href=\"includes/logout.inc.php\">Logout</a></li>";
					}
					else {
						echo "<li><a href=\"login.php\">Login</a></li>";
					}
				?>				
            </ul>
			</div>
		</nav>
		<?php
			if (isset($_SESSION["name"])){
				echo "<div id='status' style='background-color: rgb(51,204,85);'>Connected</div>";
			} else {
				echo "<div id='status' style='background-color: rgb(255,0,0);'>Disconnected</div>";
			}
		?>
		<div class=wrapper>
		

