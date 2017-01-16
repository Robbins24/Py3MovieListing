class Movie():
	""" Stores movie information """

	def __init__(self, title, year, director, actors, plot, poster, rating):
		self.title = title
		self.year = year
		self.director = director
		self.actors = actors
		self.plot = plot
		self.poster = poster
		self.rating = rating
	
	def add_director_news(self):
		director = self.director
		unformatted_output = "https://www.google.com/search?hl=en&gl=us&tbm=nws&q={director}"		
		formatted_output = unformatted_output.format(director=director)
		return formatted_output



