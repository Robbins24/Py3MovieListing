header = '''
<html lang="en">
<head>
	<title>PyMovie Share - Select Your Title</title>
  	<link rel="stylesheet" href="foundation/css/prism.css" />
  	<link rel="stylesheet" href="foundation/css/style.css" />
  	<link rel="stylesheet" href="foundation/css/shuffle-styles.css" />
  	<link rel="stylesheet" href="foundation/css/bootstrap.min.css" />  
	<link rel="stylesheet" href="foundation/css/mainCSS.css"/>	
	
	<script src="foundation/js/shuffle.js"></script>
	<script src="foundation/js/prism.js"></script>
	<script src="foundation/js/evenheights.js"></script>
	<script src="foundation/js/homepage.js"></script>
	<script src="foundation/js/jquery-3.1.1.min.js"></script>
</head>
<body style="background: url('pages/images/grey.png') repeat scroll top left" >

	<nav class="navbar navbar-inverse navbar-static-top" style="margin:0">
		<a class="navbar-brand" href="#" style="font-size:1.5em">PyMovie Share</a>
		<h4 class="status" style:"margin-left:30px; margin-top:20px">Viewing <span id="myspan"></span> Titles From Category <span id="categoryspan">All Titles</span></h4>
		<select class="sort-options" id="sorting" style="float:right">
            <option value>Default</option>
            <option value="title-az">Title (A-Z)</option>
            <option value="title-za">Title (Z-A)</option>
            <option value="date-created-desc">Year Released (New-Old)</option>
            <option value="date-created-asc">Year Released (Old-New)</option>
         </select>
         <h4 class="sortText">Sort:</h4>
		<form class="navbar-form navbar-right">
			<div class="form-group" style="margin-right:60px; margin-top:5px">
			  <input type="text" id="search" class="form-control" placeholder="Search">
			</div>
      	</form>
	</nav>

<div class="col-md-1" style="padding:0; margin-top:0; ">
	<div class="sidebar">
	<p>Poster Size</p>
	<input type="range" id="resizer" min="1" max="3" value="1" step="1"><br>
	<meta id="rownum" style="color:white"></meta>
	<p>Filter by Genre</p>
		<div class="btn-group-vertical filter-options">
    
'''

footer = '''
      <div class="col-1@md col-1@sm col-1@xs my-sizer-element"></div>
    </div>
  </div></center>
</section>

</body>
<script>
	document.getElementById("resizer").addEventListener("click", resizeFunction)
    
	function resizeFunction() {
		var slidevalue = document.getElementById("resizer").value;
		
		var newClass= "col-2@md col-2@sm col-2@xs picture-item"
		textStyle= "font-size:0.9em";
		divStyle = "height:25px;top: 87%;";

		
		 if (slidevalue == 1) {
		 		newClass = "col-2@md col-2@sm col-2@xs picture-item";
				textStyle= "font-size:0.9em";
				divStyle = "height:25px;top: 87%;";
		  } else if (slidevalue == 2) {
				newClass = "col-3@md col-3@sm col-3@xs picture-item";
				var textStyle= "font-size:1.1em"
				var divStyle = "height:35px;top: 89%;"
		  }	else if (slidevalue == 3) {
				newClass = "col-4@md col-4@sm col-4@xs picture-item";
				var textStyle= "font-size:1.1em"
				var divStyle = "height:35px;top: 89%;"
		  }	
	
		   elements = document.getElementsByName("cover");
			for (var i = 0; i < elements.length; i++) {
				elements[i].className = newClass;
			}

			textelement = document.getElementsByName("title");
			for (var i = 0; i < textelement.length; i++) {
				textelement[i].style = textStyle;
			}
			
			divelement = document.getElementsByClassName("titlediv");
			for (var i = 0; i < divelement.length; i++) {
				divelement[i].style = divStyle;
			}

			demo.shuffle.update();
			document.getElementById("rownum").innerHTML = slidevalue;
	}

</script>

</html>
'''

header_sub = '''
<html lang="en">
<head>
    <meta charset="utf-8">
	<title>PyMovie Share - Movie Page</title>
	<link rel="stylesheet" href="../foundation/css/pageCSS.css" />  	
	<link rel="stylesheet" href="../foundation/css/bootstrap.min.css" />
</head>
<body>

'''

footer_sub = '''
		

        
</body>
</html>
'''

