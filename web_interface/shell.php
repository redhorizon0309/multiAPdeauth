<?php
	include_once 'header.php';
?>
<?php
	if (isset($_SESSION["name"])){
        ?>
		<div class="container">
        	<h1>Command console</h1>
			<form action="includes/shell.inc.php" method="post">
				<label for="cmd">Command</label>
				<input type="text" id="cmd" name="cmd">
				<input type="submit" value="Submit">
			</form>
		</div>
        <?php
	}
	else {
        header("location: ../login.php");
	}
?>

		
<?php
	include_once 'footer.php';
?>