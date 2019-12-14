from product import Product
from queue import Queue
import time

class Converger:
	def __init__(self, name=''):
		self.name = name
		self.weight = 0
		self.prod_queue = Queue(maxsize=10)

	def put(self, product):
		if isinstance(product, Product):
			self.prod_queue.put(product)
			self.weight += product.weight
			print("将%s放到传送带" % product)
		else:
			print("Put on Converger Error")

	def get(self):
		prod = self.prod_queue.get()
		self.weight -= prod.weight
		return prod

	def output(self, product):
		print("传送带出口已送出：%s" % product)

	# 多线程
	def move(self, waketime=10, movetime=10):
		while True:
			time.sleep(waketime)
			if self.getWeight()>0:
				product = self.get()
				print("传送带正在运送 %s" % product)
				time.sleep(movetime)
				
				self.output(product)

	def getWeight(self):
		return self.weight


