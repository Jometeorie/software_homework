from queue import Queue
from converger import Converger
import time

class Robot:
	def __init__(self, name='', con=Converger()):
		self.name = name
		self.converger = con
		self.state = 'Fine'
		self.use = False
		self.request_queue = Queue(maxsize=10)

	# 机器人自检
	def self_check(self):
		if self.state=='Fine':
			return True
		else:
			return False

	# 机器人是否在用
	def isInUse(self):
		return self.use

	def setInUse(self):
		if self.isInUse:
			print("%s 正在使用中!" % self.name)
		else:
			self.use = True
			
	def setNotUse(self):
		if not self.isInUse:
			print("%s 未被使用!" % self.name)
		else:
			self.use = False

	# 电脑控制机器人 取工具
	# 暂时放到任务队列
	def move(self, product):
		self.request_queue.put(product)
		print("Robot.move:%s收到取工具指令" % self.name)

	# 机器人放工具到传送带上
	# 多线程 每隔dalay时间检查是否有任务
	def work(self, waketime=10, movetime=20):
		
		# print("work")
		while True:
			# 
			time.sleep(waketime)
			print("Robot.work:%s等待取工具指令" % self.name)
			if self.self_check()==False:
				print("%s出故障,暂停使用" % self.name)
				break

			if self.request_queue.qsize()>0 and self.isInUse()==False:
				print("Robot.move:%s正在取工具" % self.name)
				# 取出产品
				product = self.request_queue.get()
				# 连接数据库 获取工具是否存在
				# 假设都有。。。
				
				self.setInUse()
				time.sleep(movetime)
				self.converger.put(product)
				self.setNotUse()

		return True
		pass

			
