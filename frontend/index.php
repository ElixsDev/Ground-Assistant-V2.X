<?php
    $name = "Ground-Assistant";
    $description = "EliServices Ground-Assistant";
    $version = $_GET["version"];
    $content = file_get_contents("./content/".$version.".html");
    require "./base/template.php";
?>
