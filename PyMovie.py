
# PyMovie.py
import os
import sys
import codecs
import json
import urllib
import argparse
import webbrowser
import re
from unidecode import unidecode
import sys
import pandas as pd
import datetime
import numpy as np
from libs.html import *


# ### Set Up Logging
# 
# Sets up the logger that is used throughout the program as a means of tracking issues, successes, and metrics for each function.

import logging

logger = logging.getLogger('PyMovie')
hdlr = logging.FileHandler('Data/PyMovie_log.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel("INFO")


# ### Clean Movie Titles
# These three functions used to clean up file names that may have dates, extraneous words in parentheses, etc. By normalizing the names, we hope to have greater success when querying the IMDB API.  These different styles of normalizing are fed into the API through the getOMDB() function.
# 
# *cleanTitle3()* is used as a helper function for naming of poster files and for text output.

def cleanTitle(filename):
    title = re.sub(r'\.(\w|\d){2,4}$',"",filename) #Remove file extension
    title = re.sub(r'(\(|\[)(.*)(\)|\])',"",title) #Remove anything in parentheses or brackets
    title = re.sub(r'\:',"",title) #Remove Colons
    title = re.sub(r'(\s)?\-(\s)?'," ",title) #Remove hyphens for subtitles
    title = re.sub(r'(\s)[0-9]{1,2}(\s)', ' ',title) #Remove Numeric identifiers
    title = title.strip() #Trim Whitespace
    return title  

def cleanTitle2(filename):
    title = re.sub(r'\.(\w|\d){2,4}$',"",filename) #Remove file extension
    title = re.sub(r'(\(|\[)(.*)(\)|\])',"",title) #Remove anything in parentheses or brackets
    title = re.sub(r'\:',"",title) #Remove Colons
    title = re.sub(r'[\w\s]*(\s)?\-(\s)?',"",title) #Submit only subtitles
    title = title.strip() #Trim Whitespace
    return title


def cleanTitle3(filename):
    title = re.sub(r'\.(\w|\d){2,4}$',"",filename) #Remove file extension
    return title


# ### Build URL for API
# This function determines whether the filename contains a release year and, if so, includes the year as a parameter when searching the API. If it does not, only the title is used.

def cleanURL(filename, title):
    year = re.search(r'(\[|\()([0-9]{4})(\]|\))',filename)
    if year:
        year= re.sub(r"(\[|\(|\]|\))","", year.group(0))
    else:
        year=""
    if not year == "":
        url = "http://www.omdbapi.com/?t=" + urllib.parse.quote(title) + '&y=' + urllib.parse.quote(year) + '&tomatoes=true&type=movie'
    else:
        url = "http://www.omdbapi.com/?t=" + urllib.parse.quote(title) + '&tomatoes=true&type=movie'
    return url


# ### Retrieving From OMDB
# This function uses two of the cleantitleX() functions to normalize the movie title, feed it into the API, and, if successful, download the resulting JSON.  The API always passes back a parameter named "Response" that is True if the query returned a result and False if it did not. The function is set up to only try further responses if the intial response doesn't work. There is room for improvement in this code and I will work to clean it up as time permits.

def getOMDB(movieTitle):
    
    #First Attempt
    title = cleanTitle(movieTitle)
    url = cleanURL(movieTitle, title)
    reader = codecs.getreader("utf-8")
    data = json.load(reader(urllib.request.urlopen(url)))

    if data["Response"] == "True":
        return data
    else:
        #Second Attempt
        title = cleanTitle2(movieTitle)
        url = cleanURL(movieTitle, title)
        reader = codecs.getreader("utf-8")
        data = json.load(reader(urllib.request.urlopen(url)))

        if data["Response"] == "True":
            return data
        else:
            print("exit")
            return()


# ### Helper Function: Add '/' to end of directory
# 
# This function takes a directory name and ensure it ends with a slash (i.e., "/"). This keeps the later functions from throwing errors.

def dirClean(directory_name):
    if directory_name[-1] != "/":
        directory_name = directory_name + "/"
    return(directory_name)


# ### Helper Function: Validate User Input
# In the *crawl()* function, users are asked to enter a number. This function validates whether an acceptable input was entered.

def validateInput(response):
    if response == "":
        print("Please Enter A Value")
        return(False)
    if response.isdigit():
        response = int(response)
        if response > 0 and response < 4:
            return(True)          
        else:
            print("Please Enter One of the Values Shown")
            return(False)
    else:
        print("Please Enter a Number")
        return(False)


# ### Data Collection Function
# 
# This function reads the names of files in a provided directory and then runs those files through the IMDB API to collect movie information.  The final output are two .csv files; one for movies that were found through the API and another for files that weren't found.  This function also checks against previous runs of the function to limit the number of API calls.  Finally, this function downloads and stores movie poster artwork for later use in web page construction.

def crawl(source_dir):
    begin = datetime.datetime.now() #For recording runtime
    logger.info('crawl() START')
    
    source_dir = dirClean(source_dir)
    movie_list = os.listdir(source_dir)
    columns = ['ID','title','year','duration','release_date','mpaa_rating','director','actors','plot','genre','poster','rating_imdb','rating_metacritic','rating_rotten','awards','boxoffice','filename','filesize']
    
    startposters = len(os.listdir("./Site/pages/posters/"))
    
    #Attempt to load existing data. If it is not there, create empty dataframe instead
    if os.path.exists("Data/movieDF.csv"):
        movieDF = pd.read_csv("Data/movieDF.csv")
        startrows = len(movieDF)
        if os.path.exists("Data/failedmovieDF.csv"):
            moviefailDF = pd.read_csv("Data/failedmovieDF.csv")
        else:
            moviefailDF = pd.DataFrame(columns = ['title'])
        #Remove rows from movieDF for movies that no longer appear in the directory
        for movie in movieDF['filename']:    
            if movie not in movie_list:
                movieDF = movieDF[movieDF.filename != movie]
                logger.info("Removed " + movie + " from movie library.")
                #Remove photos for movies that no longer appear in the directory
                title = cleanTitle(movie)
                if title + '.jpg' in os.listdir("./Site/pages/posters/"):
                    os.remove('./Site/pages/posters/' + title + '.jpg')
                    logger.info('Removed ' + title + '.jpg from poster folder.')
                if title + '.html' in os.listdir("./Site/pages/"):
                    os.remove('./Site/pages/' + title + '.html')
                    logger.info('Removed ' + title + '.html from webpages folder.')
    else: 
        movieDF = pd.DataFrame(columns=columns)
        moviefailDF = pd.DataFrame(columns = ['title'])
        startrows = len(movieDF)
    
    ############ Experimenting with Optional Manual Search ################
    print("Posters, descriptions, and other metadata will now be downloaded for your movies. This script will attempt to match the filenames you gave your movies to the omdbapi.com API.  This is not an exact process and may result in errors or failures to match. Below you are given two options for completing this search.")
    print("")
    print("*  The 'Manual' search will ask you to confirm whether the omdb API match is correct and, if not, will ask prompt you to enter a new title.")
    print("*  The 'Automatic' search will use whatever movie is returned by the omdb API.")
    print("")
    print("Enter the number of the search mode you would like to use and press enter.")
    print("1. Manual Search")
    print("2. Automatic Search")
    print("3. Exit")

    valid = False
    while valid == False:
        movieResponse = input('')
        valid = validateInput(movieResponse)
    print("--------------------------------------------------")               
            
    #######################################################################
    
    
    for movie in movie_list:
                # The following 2 lines may need to be hacked at dependent of naming
                # Scheme. Or, a more dynamic solution may be needed to suffice.
                movieInfo = pd.DataFrame(columns=columns)
                title = cleanTitle(movie[0:])
                
                #If movie is already in the dataframe than skip to the next iteration of the loop
                if movie in movieDF['filename'].values:
                    #If movie poster isn't downloaded, then download it based on stored URL
                    if cleanTitle3(movie) + '.jpg' not in os.listdir("./Site/pages/posters/"):
                        print(movie)
                        print(pd.isnull(movieDF.loc[movieDF['filename'] == movie, 'poster'].values[0]))
                        if not pd.isnull(movieDF.loc[movieDF['filename'] == movie, 'poster'].values[0]):
                            os.system('wget -O "Site/pages/posters/' + cleanTitle3(movie) + '.jpg" ' + movieDF.loc[movieDF['filename'] == movie, 'poster'].values[0])
                    continue
                
                try:                   
                    if movie.startswith("."):
                        continue
                        
                    ############ Experimenting with Optional Manual Search ################
                    if movieResponse == "1":
                        movieLoop = "2"
                        searchmovie = movie
                        while movieLoop == "2":
                            data = getOMDB(searchmovie)
                            try:
                                print("")
                                print("Looking Up:  " + searchmovie)
                                print("--> " + data["Title"] + " (" + data["Year"].split(" ")[0] +")")
                                print("-->" + data["Plot"])
                                print("")
                                print("Is this the movie you wanted?")
                                print("1. Yes")
                                print("2. No")
                                print("3. Exit Metadata Search")
                                valid = False
                                while valid == False:
                                    movieLoop = input('Is this the movie you wanted?:')
                                    valid = validateInput(movieLoop)
                            except:
                                print("")
                                print("--> Movie Not Found")
                                movieLoop = "2"

                            if movieLoop == "3":
                                data=[]
                                movieResponse = "3"
                                break
                            
                            if movieLoop== "2":
                                print("")
                                searchmovie = input('Try a different title (or type "next" to move on):')

                            if movieLoop == "1" or searchmovie == "next":
                                print("--------------------------------------------------")
                                break
                    if movieResponse == "2":
                            data = getOMDB(movie)
                            print("Searching for:  " + cleanTitle3(movie))
                    if movieResponse == "3":
                        continue
                    #######################################################################


                    try:
                        movie_imdbID = data["imdbID"]
                        movie_title = unidecode(data["Title"])
                        movie_year = data["Year"].split(" ")[0]
                        movie_duration = data["Runtime"]
                        movie_release = data["Released"]
                        movie_director = unidecode(data["Director"])
                        movie_actors = unidecode(data["Actors"])
                        movie_plot = unidecode(data["Plot"])
                        movie_genre = data["Genre"]
                        movie_poster = data["Poster"]
                        movie_rating = data["Rated"]
                        movie_awards = data["Awards"]
                        movie_money = data["BoxOffice"]
                        
                        #If poster file doesn't exist in image directory then download it based on API URL
                        if cleanTitle3(movie) + '.jpg' not in os.listdir("./Site/pages/posters/"):
                            filename = cleanTitle3(movie)
                            os.system('wget -O "Site/pages/posters/' + filename + '.jpg" ' + movie_poster)
                        
                        movie_rating_imdb = data["imdbRating"]
                        movie_rating_metacritic = data["Metascore"]
                        movie_rating_rotten = data["tomatoMeter"]
                        movie_filename = movie
                        
                        movie_filesize = os.path.getsize(source_dir + movie)                   
                        

                        movieInfo.loc[1] = [movie_imdbID, movie_title, movie_year, movie_duration, movie_release, movie_rating, movie_director, movie_actors, 
                                            movie_plot, movie_genre,movie_poster, movie_rating_imdb, movie_rating_metacritic, 
                                            movie_rating_rotten, movie_awards, movie_money, movie_filename, movie_filesize]
                        
                        movieDF = movieDF.append(movieInfo)
                        
                        logger.info("Success - " + movie)
                        
                    except Exception as e:
                        failMovie = pd.DataFrame(columns=['title'])
                        failMovie.loc[1] = title
                        moviefailDF = moviefailDF.append(failMovie)
                        print(e)
                        logger.info("Failed - " + movie)
                        pass
                except Exception as e:
                    print(e)
    movieDF = movieDF.sort_values(by='title')
    movieDF.to_csv('Data/movieDF.csv',index=False)
    moviefailDF.to_csv('Data/failedmovieDF.csv',index=False)
    
    #write to Logger
    run_columns = ['date','time','runtime','movie_delta','movie_total','poster_delta','poster_total']
    
    if os.path.exists("Data/runData.csv"):
        run_data = pd.read_csv("Data/runData.csv")
    else: 
        run_data = pd.DataFrame(columns=run_columns)
        
    end = datetime.datetime.now()
    endrows = len(movieDF)
    endposters = len(os.listdir("./Site/pages/posters/"))
    now = datetime.datetime.now()
    
    runInfo = pd.DataFrame(columns=run_columns)
    runInfo.loc[1] = [now.strftime('%Y-%m-%d'),now.strftime('%H:%M:%S'),end-begin, 0-(startrows-endrows),endrows,
                     0-(startposters-endposters), endposters]
    run_data = run_data.append(runInfo)
    run_data.to_csv('Data/runData.csv',index=False)
    
    logger.info('Crawl() function complete')
    print("crawl() END")


# ### UI Building Function
# 
# This function creates a website that has a main page that displays movie posters and names and then subpages for each movie that was successfully found through the IMDB API. Added a jquery table that allows the user to sort and search for movies based on title, genre and rating.

def htmlout(movie_file, source_dir):
    logger.info('htmlout() START')
    
    movieDF = pd.read_csv("Data/" + movie_file)
    output_file = "Site/movies.html"
    
    movieDF['genre_all'] = None
    for row in range(0,movieDF.shape[0]):
        movieDF.ix[row, 'genre_all'] = str(movieDF.ix[row, 'genre'].lower().split())
        movieDF.ix[row, 'genre_all'] = re.sub(",'",'"',movieDF.ix[row, 'genre_all'])
        movieDF.ix[row, 'genre_all'] = re.sub("'",'"',movieDF.ix[row, 'genre_all'])
    
    try:
        # Opening and generating final html (for example movies.html) file
        html_file = open(output_file, "w")
        html_file.write(header)
        
        #Add Button Group
        allgenre = []
        for movie in movieDF['genre']:
            allgenre += movie.split(",")
        allgenre = np.sort(list(set(allgenre)))
        
        for genre in allgenre:
            html_file.write('<button class="filterButton" data-group="' + genre.lower().strip() + '">' + genre.strip() + '</button>')
        html_file.write('</div></div></div>')
        
        #Add Content Sections
        html_file.write('<div class ="col-md-11" style="padding-bottom:30px">')
        html_file.write('<section id="demo"><center>')
        html_file.write('<div class="container">')
        html_file.write('<div id="grid" class="row my-shuffle-container">')

        for index, row in movieDF.iterrows():
            title = cleanTitle(row['filename'])
            
            html_file.write("<figure name='cover' class='col-2@md col-2@sm col-2@xs picture-item' data-groups='" + row['genre_all'] + "' data-date-created='" + str(row['year']) + "-06-01' data-title='" + row['title'] + "'>")
            html_file.write('<div class="picture-item__inner">')
            html_file.write('<div class="aspect aspect--2x3">')
            html_file.write('<div class="aspect__inner">')
            if cleanTitle3(row['filename']) + '.jpg' in os.listdir("./Site/pages/posters/"):
                html_file.write('<a href="./pages/'+ title + '.html"><img src="pages/posters/' + cleanTitle3(row['filename']) + '.jpg" class="face pic"/></a>')
            else:
                html_file.write('<a href="./pages/'+ title + '.html"><img src="pages/images/NA.jpg" class="face pic"/></a>')
            html_file.write('</div>')
            html_file.write('</div>')
            html_file.write('<div class="titlediv" style="height:25px;top: 87%;">')
            html_file.write('<figcaption name="title" class="titletext" style="font-size:0.9em"><a href="./pages/' + title + '.html" target="_blank">' + title + '</a></figcaption>')
            html_file.write('</div>')
            html_file.write('</div>')
            html_file.write('</figure>')
        
        html_file.write(footer)
        html_file.close()
        logger.info("Homepage Complete")
        
        #Create SubPages        
        for index, row in movieDF.iterrows():
            title = cleanTitle(row['filename'])
            
            movie_page = "./Site/pages/" + title + ".html"     
            html_file = open(movie_page, "w")
            html_file.write(header_sub)
            
            if cleanTitle3(row['filename']) + '.jpg' in os.listdir("./Site/pages/posters/"):
                html_file.write('<img src="posters/' + cleanTitle3(row['filename']) + '.jpg" class="img-bk"/>')
            html_file.write('<a href="../movies.html"><img src="images/backarrow.png" class="back-button"/></a>')
                
            html_file.write('<div id="content">')
            html_file.write('<div class="col-md-4">')
            if cleanTitle3(row['filename']) + '.jpg' in os.listdir("./Site/pages/posters/"):
                html_file.write('<img src="posters/' + cleanTitle3(row['filename']) + '.jpg" class="coverart"/>')
            else:
                html_file.write('<img src="images/NA.jpg" class="coverart" />')
                
            html_file.write('</div>')
            html_file.write('<div class ="col-md-8" style="padding-left:30px; padding-right:30px"><br>')
            html_file.write('<p class="titleshadow" id="movie">' + str(row['title']) + '</p><p class="movieyear" id="year">' + str(row['year']) + '</p>') 
            html_file.write('<hr class="title-border">') 
            html_file.write('<p class="runtime" id="runtime">' + str(row['duration']) + '</p><p class="genres" id="genre">' + str(row['genre']) +'</p><br><br>')
            
            html_file.write('<div class ="col-md-9"><br>')
            html_file.write('<p class="elements">Plot: </p> <p class="desctext">' + str(row['plot']) + '</p><br><br>')
            html_file.write('<p class="elements">Actors: </p> <p class="desctext">' + str(row['actors']) + '</p><br><br>')
            html_file.write('<p class="elements">Director: </p> <p class="desctext">' + str(row['director']) + '</p><br><br>')
            html_file.write('<p class="elements">Release Date: </p> <p class="desctext">' + str(row['release_date']) + '</p>')
            
            html_file.write('<hr>')
            html_file.write('<a href="file://' + dirClean(source_dir) + row['filename'] + '" download><img src="images/download.png" class="icons"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="file://' + dirClean(source_dir) + row['filename'] + '"><img src="images/play.png" class="icons"></a>')
              
            html_file.write('</div>')
            html_file.write('<div class ="col-md-3"><br>')
            
            #Ratings Pane
            ##MPAA Rating
            html_file.write('<center><span class="mpaa">' + str(row['mpaa_rating']) + '</span></center><hr>')
            ##IMDB Rating
            html_file.write('<center><p class="rating" style="padding-bottom: 2px"><b>IMDB</b><br>' + str(row['rating_imdb']) + '/10</p></center><hr>')
            ##Metacritic Rating
            html_file.write('<center><p class="rating" style="padding-bottom: 2px"><b>Metacritic</b></p>')           
            if row['rating_metacritic'] <= 20: 
                html_file.write('<span class="metalow">' + str(int(row['rating_metacritic']))+'</span></center>')
            elif 20 < row['rating_metacritic'] <= 40: 
                html_file.write('<span class="metamedlow">' + str(int(row['rating_metacritic']))+'</span></center>')   
            elif 40 < row['rating_metacritic'] <= 60: 
                html_file.write('<span class="metamedium">' + str(int(row['rating_metacritic']))+'</span></center>')    
            elif 60 < row['rating_metacritic'] <= 80: 
                html_file.write('<span class="metamedhigh">' + str(int(row['rating_metacritic']))+'</span></center>')    
            elif row['rating_metacritic'] > 80: 
                html_file.write('<span class="metahigh">' + str(int(row['rating_metacritic']))+'</span></center>') 
            else:
                html_file.write('<span class="metaNA">NA</span></center>')
            html_file.write('<hr>')
            
            ##Rotten Tomatoes
            html_file.write('<center><p class="rating" style="padding-bottom: 2px"><b>Rotten Tomatoes</b><br>' + str(row['rating_rotten']) + " ")
            if row['rating_rotten'] < 60: 
                html_file.write('<img src="images/rottenicon.png" style="width:30px; display:inline"></p></center>') 
            elif row['rating_rotten'] >= 60: 
                html_file.write('<img src="images/freshicon.png" style="width:30px; display:inline"></p></center>')
            else:
                html_file.write('</p></center>')

            html_file.write('</div></div></div>')

            html_file.write(footer_sub)
            html_file.close()
            logger.info("Success - " + title + '.html')
        
        # Opening the browser and presenting the summary html page
        webbrowser.open('file://' + os.path.realpath(output_file))
    except Exception as e:
        print(e)
        traceback.print_tb(e)
        print("***** Error. Maybe try to run the script again but bit later? *****")
        logger.critical('Critical error -- Abort Script')
        sys.exit(0)
        
    #write to Logger
    logger.info('htmlout() function complete')
    print("htmlout() END")

