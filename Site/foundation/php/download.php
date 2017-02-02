<?php
  $file = 'mylog.txt';
//Get movie title
	$url = $_SERVER['HTTP_REFERER'];
    $html = file_get_contents($url);
    $doc = new DOMDocument(); // create DOMDocument
    libxml_use_internal_errors(true);
    $doc->loadHTML($html); // load HTML you can add $html
    $movie = $doc->getElementByID('movie') -> nodeValue;

// Append a new person to the file
$current = "DOWNLOAD, " . $movie . ", " . date("Y-m-d") . ", " . date("h:i:sa") . ", " . $_SERVER['REMOTE_ADDR'];
// Write the contents back to the file
file_put_contents($file, $current . PHP_EOL, FILE_APPEND);
  ?>