<?php
	session_start();
?>
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Master Controller</title>
		<link rel="stylesheet" type="text/css" href="style.css">
	</head>
	<body>
	    <nav>
			<div class="wrapper">
			<a href="index.php"></a>
			<ul>
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

