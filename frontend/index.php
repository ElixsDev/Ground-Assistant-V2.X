<?php
    $name = "Ground-Assistant";
    $description = "EliServices Ground-Assistant";
    $version = $_GET["version"];
    if ($version != "stable" and $version != "unstable" and $version != "2021") {
        $version = "stable";
    }
    $content = "./content/".$version.".php";
    require "./base/template.php";
?>
