<?php
	include_once 'header.php';
?>
			<div class="container">
				<h1>Login</h1>
				<form action="includes/login.inc.php" method="post">
	    		    <label>Name</label>
	    		    <input type="text" name="name" placeholder="name">

	    		    <label>Password</label>
	    		    <input type="text" name="password" placeholder="password">

	    		    <button type="submit" name="submit">Login</button>
	    		</form>
			</div>
			<?php
if (isset($_GET["error"])) {
	if ($_GET["error"] == "emptyinput") {
		echo "<p>Empty field!</p>";
	}
	elseif ($_GET["error"] == "wronglogin") {
		echo "<p>Wrong username!</p>";
	}
	elseif ($_GET["error"] == "wrongpassword") {
		echo "<p>Wrong password!</p>";
	}
	elseif ($_GET["error"] == "stmtfailed") {
		echo "<p>Something went wrong, try again!</p>";
	}
	elseif ($_GET["error"] == "none") {
		echo "<p>Success!</p>";
	}
}
?>

<?php
	include_once 'footer.php';
?>