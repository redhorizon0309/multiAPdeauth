<?php
	include_once 'header.php';
?>
<?php
	if (isset($_SESSION["name"])){
		$iam = shell_exec("whoami");
		function liveExecuteCommand($cmd) {
    	while (@ ob_end_flush()); // end all output buffers if any

    	$proc = popen("$cmd 2>&1 ; echo Exit status : $?", 'r');

    	$live_output     = "";
    	$complete_output = "";

    	while (!feof($proc))
    	{
    	    $live_output     = fread($proc, 4096);
    	    $complete_output = $complete_output . $live_output;
    	    echo "$live_output";
    	    @ flush();
    	}

    	pclose($proc);

    	// get exit status
    	preg_match('/[0-9]+$/', $complete_output, $matches);

    	// return exit status and intended output
    	return array (
    	                'exit_status'  => intval($matches[0]),
    	                'output'       => str_replace("Exit status : " . $matches[0], '', $complete_output)
    	             );
		}

        ?>
		<div class="container">
        	<h1>Command console</h1>
			<div class="row">
				<form method="post">
					<?php
						echo "<label for='cmd'>$iam $ </label>";
					?>
					<input type="text" id="cmd" name="cmd" class="cmd">
					<input name="submit" type="submit" value="submit">
				</form>
			</div>		
		</div>
		<div class="container">
        	<?php
				if (isset($_POST["cmd"])) {
					echo "<h2>Response:</h2>";
					$cmd = $_POST["cmd"];
					//$output = shell_exec($cmd);
					$output = shell_exec($cmd);
					echo "<pre>$output</pre>";
				}
			?>
		</div>
<?php
	}

?>

		
<?php
	include_once 'footer.php';
?>