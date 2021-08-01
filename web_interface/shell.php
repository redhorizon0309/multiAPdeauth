<?php
	include_once 'header.php';
?>
<?php
	if (isset($_SESSION["name"])){
        ?>
        <h1>Command console</h1>
			<form action="shell.php" method="post">
				<label for="cmd">Cmd</label>
				<input type="text" id="cmd" name="cmd">

				<input type="submit" value="Submit">
			</form>
        <?php
	}
	else {
        header("location: ../login.php");
	}
?>

		
<?php
	include_once 'footer.php';
?>