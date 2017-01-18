#!/usr/bin/env python

#########################################################################
# Py3 Movie Directory Listing / SyntaxErrorz12 / Python 3.5 / 2016
# Based on original work of Github: sikor80/python-movie-catalog-generator
# Originally for Python 2.
#########################################################################

import os
import json
import codecs
import urllib
from urllib.parse import *
from urllib.request import *
import argparse
import webbrowser
import sys
import traceback
import logging

# Local Libs
from libs.media import *
from libs.html import *


def main():
    desc = """
    ###############################################
    Py3 Movie Directory Listing - SyntaxErrorz 2017
    Originally based on: python-movie-catalog-generator

    Python script which scans a directory, parses titles against OmdbAPI, and provides an HTML directory listing

    REQUIREMENTS:
    - Python 3.5
    - Active Internet connection
    - Ideally each of the movie files needs to be stored in a separate folder.
    - Naming convention should only include movie title. Modification to the script can be made to adhere to differnet naming standards.


    USAGE:
    - Run python main.py [DIR]
    - [DIR] should be the directory where the movies are present.
    - HTML file outputs to the same directory as the script without modification to the current code base.

    ###############################################
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('directory', help='the directory to search for movie files')

    args = parser.parse_args()

    source_dir = args.directory
    if not os.path.isdir(source_dir):
        print(desc)
        print("Error: please supply a directory")
        sys.exit(0)
    print(desc)
    data = crawl(source_dir)
    htmlout(*data, source_dir)


def crawl(source_dir):
    try:

        output_file = "movies.html"

        movie_list = os.listdir(source_dir)
        movie_objects_list = []
        failed_movie_objects_list = []

        # Combing through each movie and pulling ombdapi JSON Data for them.
        for movie in movie_list:
            # The following 2 lines may need to be hacked at dependent of naming
            # Scheme. Or, a more dynamic solution may be needed to suffice.
            title = movie[0:]
            # year = movie[-6:][1:-1]
            try:
                # Using API from http://www.omdbapi.com/
                url = "http://www.omdbapi.com/?t=" + urllib.parse.quote(title)  # + "&y=" + year
                # Now dowloading and parsing the results as json file so we can work on it locally
                reader = codecs.getreader("utf-8")
                data = json.load(reader(urllib.request.urlopen(url)))

                try:
                    movie_imdbID = data["imdbID"]
                    # Adding .encode('utf8') otherwise, python errors out parsing non-ascii chars
                    movie_title = data["Title"]
                    movie_year = data["Year"]
                    movie_director = data["Director"].encode('utf8')
                    movie_actors = data["Actors"].encode('utf8')
                    movie_plot = data["Plot"].encode('utf8')
                    movie_poster = data["Poster"]
                    # movie_poster_local = urllib.request.urlretrieve(movie_poster, movie_poster)
                    movie_rating = data["imdbRating"]
                    # movie_object_name = "movie_" + movie_imdbID
                    movie_object_name = Movie(movie_title, movie_year, movie_director, movie_actors, movie_plot,
                                              movie_poster, movie_rating)

                    movie_objects_list.append(movie_object_name)
                    print("Success - " + movie)
                    logging.info("Success - " + movie)
                    # Following line added for debugging the OMDBAPI Calls.
                    print("URL: " + url)
                except Exception as e:
                    failed_movie_objects_list.append(movie)
                    print("URL: " + url)
                    print("Failed - " + movie)
                    print(e)
                    logging.info("Failed - " + movie)
                    pass
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print("***** Error. Maybe try to run the script again but bit later? *****")
        logging.critical('Critical error -- Abort Script')
        sys.exit(0)
    finally:
        return movie_objects_list, failed_movie_objects_list, output_file


def htmlout(movie_objects_list, failed_movie_objects_list, output_file, source_dir):
    try:

        # Opening and generating final html (for example movies.html) file
        html_file = open(output_file, "w")
        html_file.write(header)

        for movie_object in movie_objects_list:
            news = movie_object.add_director_news()

            html_file.write('<div class="row">')
            html_file.write('<div class="medium-4 columns">')
            html_file.write('<div class="panel">')
            html_file.write('<img src="' + movie_object.poster + '" />')
            html_file.write('</div></div>')
            html_file.write('<div class="medium-8 columns">')
            html_file.write('<div class="panel">')
            html_file.write(
                '<a href="file://' + source_dir + '\test" class="button large success expand">' + movie_object.title + ' (' + movie_object.year + ')' + '</a>')
            html_file.write("<p><b>Plot:</b> " + str(movie_object.plot) + "</p>")
            html_file.write("<p><b>Actors:</b> " + str(movie_object.actors) + "</p>")
            html_file.write('<p><b>Director:</b> ' + str(
                movie_object.director) + '<a href="' + news + '"> - Google News</a></p>')
            html_file.write("<p><b>Rating:</b> " + str(movie_object.rating) + "</p>")

            html_file.write("</div></div></div>")

        # Generate some stats at on the bottom of the html page
        html_file.write('<div class="row">')
        html_file.write('<hr>')
        html_file.write('<p> Directory scanned: ' + str(os.getcwd()) + '/' + source_dir + '</p>')
        html_file.write('<p> Success entries: ' + str(len(movie_objects_list)) + '</p>')
        html_file.write('<p> Movies Without IMDB Data: ' + str(len(failed_movie_objects_list)) + '</p>')
        for number in range(len(failed_movie_objects_list)):
            html_file.write('<a href="#" class="button large success expand">' + str(
                failed_movie_objects_list[number]) + '</a><br/> ')

        html_file.write(footer)
        html_file.close()

        # Opening the browser and presenting the summary html page
        webbrowser.open('file://' + os.path.realpath(output_file))
    except Exception as e:
        print(e)
        print("***** Error. Maybe try to run the script again but bit later? *****")
        logging.critical('Critical error -- Abort Script')
        sys.exit(0)

if __name__ == "__main__":
    main()
