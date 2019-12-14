
class Computer:
	def __init__(self, name=None, robots=[]):
		self.name = name
		self.robots = robots

	def check(self, name):
		# 数据库读取名字
		# 验证用户是否存在
		return True

	def fetchProd(self, product):
		# print("hhh")
		# hasGot = False
		for robot in self.robots:
			# print("hhhh")
			if robot.self_check()==True and robot.use==False:
				# print("hhhhhh")
				# 标记机器人正在运送
				# robot.setInUse()
				robot.move(product)
				break
		# print("fetchProd")
		# print(hasGot)
		# return hasGot

	def control(self, computer):
		pass
		# for item in prod_list

	def addRobot(self, robot):
		self.robots.append(robot)

	def delRobot(self, robot):
		index = robots.index(robot)
		if index!=-1:
			self.robots.pop(index)

		



