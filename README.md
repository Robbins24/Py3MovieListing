# PyMovie Share
Python 3 based Dir to HTML Movie listing generator (IMDB Details)

	###############################################
	Py3 Movie Directory Listing - SyntaxErrorz 2017
	Originally based on: python-movie-catalog-generator

	Python script which scans a directory, parses titles against OmdbAPI, and provides an HTML directory listing

	REQUIRMENTS:
	- Python 3.5
	- Active Internet connection when running crawl() function. The data will be stored for later use by the htmlout() function
	- Naming convention can include movie title and year in parentheses (e.g., Arrival (2016).mp4). Modification to the script can be made to adhere to differnet naming standards.


	USAGE:
	- Run python PyMovieRun.py, the program will ask you to input a movie directory.
	- The directory should be the directory where the movies are present.
	- A self-contained website is built in the directory "Site". There will be a "movies.html" file in the main directory and a number of subpages output to the 'pages' folder.
  	- On the main page, there is a shuffle.js array of movie posters. The array is searchable, sortable, and filterable. Users then navigate to a subpage with more detailed info where they can either download the movie or stream depending on their browser.
  	
  FUTURE RELEASE MODS:
  - Clean up the file name convention/process
	###############################################
