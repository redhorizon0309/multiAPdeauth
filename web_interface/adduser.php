<?php
	include_once 'header.php';
?>
			<div class="container">
				<h1>Add user</h1>
				<form action="includes/adduser.inc.php" method="post">
	    		    <label>NewUser</label>
	    		    <input type="text" name="name" placeholder="name">
	
	    		    <label>Password</label>
	    		    <input type="text" name="password" placeholder="password">
	
	    		    <label>Password</label>
	    		    <input type="text" name="passwordRepeat" placeholder="repeat password">
	    		    
            	    <button type="submit" name="submit">Add User</button>
	    		</form>
			</div>
            
<?php
if (isset($_GET["error"])) {
	if ($_GET["error"] == "emptyinput") {
		echo "<p>Empty field!</p>";
	}
	elseif ($_GET["error"] == "invalidname") {
		echo "<p>Invalid name!</p>";
	}
	elseif ($_GET["error"] == "pwdmismatch") {
		echo "<p>Repeat password mismatch</p>";
	}	
	elseif ($_GET["error"] == "invalidpass") {
		echo "<p>Invalid password!</p>";
	}
	elseif ($_GET["error"] == "namexisted") {
		echo "<p>Choosen name already existed!</p>";
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