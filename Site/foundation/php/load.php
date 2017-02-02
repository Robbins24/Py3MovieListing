<?php
  	$file = 'mylog.txt';
  
	//Get webpage
	preg_match_all('/[\w\%]*.html$/',$_SERVER['HTTP_REFERER'], $output, PREG_PATTERN_ORDER);

	// Append a new person to the file
	$current = "LOAD, " . $output[0][0] . ", " . date("Y-m-d") . ", " . date("h:i:sa") . ", " . $_SERVER['REMOTE_ADDR'];
	// Write the contents back to the file
	file_put_contents($file, $current . PHP_EOL, FILE_APPEND);
  ?>