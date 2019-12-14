from random import random

class Product:
	def __init__(self, name, id='',  expensive=False):
		self.id = id
		self.name = name
		self.expensive = expensive
		self.weight = random()*100

	def __str__(self):
		return self.name

	