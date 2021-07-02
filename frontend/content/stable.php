<p>Welcome to the EliServices DataAccess Page! If you find any mistake or if you have any suggestions, feel free to contect me via:            
<p><b>&nbsp &nbsp eliservices.server@gmail.com</b></p>

<!--<?php require "./dbstart.php"; ?>-->
<div id="reload"></div>

<script type="text/javascript">
    $(document).ready(function() {
        attachment = '<?php echo $sql ?>';
        $('#reload').load("./content/time.php");
        setInterval(function() {
            $('#reload').load("./content/time.php");
        } ,1000);
    })
</script>

</div>
