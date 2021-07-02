<!DOCTYPE html>
<html lang="en">
    <head>
        <?php require "./base/head.php"; ?>
    </head>
    <body>
        <?php
            require "./base/header.php";
            echo "\n";
            echo "        <div id=\"main\">\n";
            require $content;
            echo "\n";
            echo "        </div>";
            echo "\n\n";
            require "./base/footer.php";
        ?>
    </body>
</html>
