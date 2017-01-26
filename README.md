# Py3MovieListing
Python 3 based Dir to HTML Movie listing generator (IMDB Details)

	###############################################
	Py3 Movie Directory Listing - SyntaxErrorz 2017
	Originally based on: python-movie-catalog-generator

	Python script which scans a directory, parses titles against OmdbAPI, and provides an HTML directory listing

	REQUIRMENTS:
	- Python 3.5
	- Active Internet connection when running crawl() function. The data will be stored for later use by the htmlout() function
	- Naming convention should only include movie title. Modification to the script can be made to adhere to differnet naming standards.


	USAGE:
	- Run python PyMovieRun.py, the program will ask you to input a movie directory.
	- The directory should be the directory where the movies are present.
	- An HTML file outputs to the same directory as the script and a number of subpages are output to the 'pages' folder without modification to the current code base.
  	- On the main page, a sortable/searchable jquery table displays basic info about the movies. Users then navigate to a subpage with more detailed info where they can either download the movie or stream depending on their browser.
  	
  FUTURE RELEASE MODS:
  - Dump data into clean table solution which is live sortable with jquery search.
  - Clean up the file name convention/process
	###############################################
