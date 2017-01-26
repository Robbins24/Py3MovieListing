
# import movie functions

from PyMovie import crawl, htmlout, cleanTitle


# Asks for source directory and then collects movies

source_directory = input('Enter your directory:')
crawl(source_directory)


# Build Webpage

htmlout("movieDF.csv", source_directory)

