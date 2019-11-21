#!/usr/bin/env python3
# coding: utf-8


from os import system

try:
	from coulomb_counter_cc75 import Coulomb_counter
	from rospy import Publisher, init_node, is_shutdown, ROSInterruptException
except ImportError:
	system("python3 -m pip install coulomb_counter_cc75 rospkg --user")
	from coulomb_counter_cc75 import Coulomb_counter
	from rospy import Publisher, init_node, is_shutdown, ROSInterruptException

from coulomb_counter_cc75_ros.msg import Coulomb_counter_cc75 as Msg


class Coulomb_counter_ROS(Coulomb_counter):
	def __init__(self, port: str):
		Coulomb_counter.__init__(self, port)
		self.initROS()

	def initROS(self):
		init_node("coulomb_counter_cc75_manager")
		self.publisher = Publisher("coulomb_counter_cc75", Msg, queue_size=10)
		self.msg = Msg()

	def onUpdate(self):
		if is_shutdown():
			self.stop()
		for data in self:
			if data["name"] not in ("First byte", "Check sum"):
				getattr(self.msg, data["name"].lower().replace(" ", "_")).value = data["value"]
				getattr(self.msg, data["name"].lower().replace(" ", "_")).unit = data["unit"]
		self.msg.power.value = round(self.msg.voltage.value * self.msg.current.value, 2)
		self.msg.power.unit = "W"
		self.publisher.publish(self.msg)


if __name__ == "__main__":
	coulomb_counter = Coulomb_counter_ROS("/dev/coulomb_counter_cc75")
	try:
		coulomb_counter.launch()
	except KeyboardInterrupt:
		pass
	finally:
		coulomb_counter.stop()
