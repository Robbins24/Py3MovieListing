header = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <center><title>PyMovie Share</title></center>
    
    <link rel="stylesheet" href="foundation/css/foundation.min.css" />
    <link rel="stylesheet" href="foundation/css/foundation-icons.css" />
    <link rel="stylesheet" href="foundation/css/custom.css" />
    <link rel="stylesheet" type="text/css" href="foundation/css/jquery.dataTables.min.css"/>
    <script type="text/javascript" charset="utf8" src="foundation/js/jquery-3.1.1.min.js"></script>
    <script type="text/javascript" charset="utf8" src="foundation/js/jquery.dataTables.min.js"></script>

    <script type="text/javascript">
		function pgload() {
    		$.get("./foundation/php/load.php");
    		return false;
		}
	</script>
	
    <script>
   	 	$(document).ready( function () {
   		 	$('#movieTable').DataTable({
   		 	"columnDefs": [
    			{ "width": "20%", "targets": 0 },
    			{ "visible": false, "targets": 6 }
  			],
   		 	"paging":   false
   		 	});
		} );
    </script>
</head>

<body style="background: url('pages/images/grey.png') repeat scroll top left;" onload="pgload();">	
	<div class="row">	
      <div class="medium-12 columns">
 

        </div>
    </div>
    
    
'''

footer = '''
		

        
</body>
</html>
'''

header_sub = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <center><title>PyMovie Share</title></center>
    
    <link rel="stylesheet" href="../foundation/css/foundation.min.css" />
    <link rel="stylesheet" href="../foundation/css/foundation-icons.css" />
    <link rel="stylesheet" href="../foundation/css/custom.css" />
    <script type="text/javascript" charset="utf8" src="../foundation/js/jquery-3.1.1.min.js"></script>
    
    <script type="text/javascript">
		function dnld() {
    		$.get("./../foundation/php/download.php");
    		return false;
		}
	</script>

    <script type="text/javascript">
		function pgload() {
    		$.get("./../foundation/php/load.php");
    		return false;
		}
	</script>
	
</head>

<body style="background: url('images/grey.png') repeat scroll top left;" onload="pgload();">	
	<div class="row">	
      <div class="medium-12 columns">
 

        </div>
    </div>
    
    
'''

footer_sub = '''
		

        
</body>
</html>
'''

