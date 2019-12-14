from computer import Computer
from queue import Queue
import time
class Person:
	def __init__(self, name=None):
		self.name = name


class User(Person):
	def __init__(self, name):
		super(User, self).__init__(name)
	# 借用工具
	def borrow(self, admin, product):
		admin.inform(self.name, product)



class Admin(Person):
	def __init__(self, name, computer=Computer()):
		super(Admin, self).__init__(name)
		self.computer = computer
		self.request_queue = Queue(maxsize=10)
		# self.prod_list = dict()
		# prod_list['user'] = 'product'
	
	# 管理员管理多线程
	# 当有用户借工具，在电脑上去拿工具
	def manage(self, waketime=1):
		
		while True:
			time.sleep(waketime)
			print("Admin.manage:管理员等待新的请求...")
			if not self.request_queue.empty():
				print("Admin.manage:管理员请求队列有新的请求...")
				lis = self.request_queue.get()
				user_name = lis[0]
				product = lis[1]
				self.computer.fetchProd(product)
				print("%s: 你借用的 %s 正在处理..." % (user_name, product))
				# # if hasGot==True:
				# 	print("%s: you successfully got the %s" % (user_name, product))
				# else:
				# 	print("Not Found!")

	def addRobot(self, robot):
		self.computer.addRobot(robot)

	def delRobot(self, robot):
		self.computer.delRobot(robot)

	# 供用户borrow调用函数
	def inform(self, user, product):
		# 验证用户是否在数据库
		if self.computer.check(user):
			self.request_queue.put([user, product])
			return True
		else:
			return False




