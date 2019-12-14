from person import User
from person import Admin
from computer import Computer
from robot import Robot
from converger import Converger
from product import Product
import _thread
import time

def init():
	computer = Computer("Zong's Computer")
	admin = Admin("Zong", computer)

	products = []
	products.append(Product("14314", "锤子"))
	products.append(Product("241432", "螺丝刀"))
	products.append(Product("441413", "剪刀"))
	products.append(Product("534134", "钳子"))
	products.append(Product("534134", "挖掘机", expensive=True))

	converger = Converger("永不罢工的传送带")
	robots = []
	robots.append(Robot("1号机器人", converger))
	robots.append(Robot("2号机器人", converger))
	robots.append(Robot("3号机器人", converger))

	computer.addRobot(robots[0])
	computer.addRobot(robots[1])
	computer.addRobot(robots[2])

	return TWS(admin, computer, robots,products, converger)

class TWS:
	def __init__(self, admin, computer, robots, products, converger):
		self.admin = admin
		self.computers = computer
		self.robots = robots
		self.products = products
		self.converger = converger

	def run(self, user, product):

	#	print("try")
		user.borrow(self.admin, product)
	#	user.borrow(self.admin, Product("螺丝刀"))


	#	zong = User("Zong")
	#	zong.borrow(self.admin, Product("挖掘机"))

		try:
			_thread.start_new_thread(self.admin.manage, (3,))
			_thread.start_new_thread(self.robots[0].work, (2, 5))
			_thread.start_new_thread(self.robots[1].work, (2, 5))
			_thread.start_new_thread(self.robots[2].work, (2, 5))
			_thread.start_new_thread(self.converger.move, (1, 4))
		except:
			print ("Error: 无法启动线程")
		
		
		time.sleep(30)
	


# MY_TWS = None
# MY_TWS = init()
# user = User("Zhang")

# MY_TWS.run(user, Product("Something"))

if __name__ == '__main__':
    while True:
        global MY_TWS
        MY_TWS = init()
        time.sleep(100)

