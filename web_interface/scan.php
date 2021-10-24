<?php
    include_once 'header.php';
    require_once 'includes/apstable.inc.php';
?>
			<div class="container">
                <div class="row">
                    <div class="col-12">
                        <h1 class="header">Scanner</h1>
                        <?php
                            if(isset($_POST['scan'])) {
                                $arg = "bash scan.sh";
                                $result = shell_exec("$arg");
                            } else if (isset($_POST['deauth'])) {
                                $count = $_POST['deauth'];
                                echo "<p>$count</p>";
                                $arg = "bash deauth.sh $count";
                                $result = shell_exec("$arg");
                            } else if (isset($_POST['select'])) {
                                $id = $_POST['select'];
                                $arg = "python3 APshandler.py 1 $id";
                                $result = shell_exec("$arg");
                            } else if (isset($_POST['deselect'])) {
                                $id = $_POST['deselect'];
                                $arg = "python3 APshandler.py 2 $id";
                                $result = shell_exec("$arg");
                            }
                        ?>
                        <form method='post'>
                            <button name='scan' type='submit' class='left' value='scan'>Scan</button>
                            <input name='deauth' type='number' class='right'>
                            <button name='deauth' type='submit' class='right' value='deauth'>Deauth</button>
                        </form>
                        
                        <h2><span>APs</span>: <span id="apNum"></span></h2>
                        <?php
                            scan();
                        ?>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                            <table id="apTable">
                                <?php
                                    drawTable();
                                ?>
                            </table>
                    </div>
                </div>
			</div>

<?php
	include_once 'footer.php';
?>