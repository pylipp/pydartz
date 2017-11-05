#! /usr/bin/env python

import rospy
from std_msgs.msg import String
from dart_node.srv import GetInput

from pydarts.communication import RosCommunicator
from pydarts.game import Game


class DartNode(object):

    def __init__(self):
        self.print_output_publisher = rospy.Publisher("/print_output", String,
                queue_size=None)

        rospy.wait_for_service("/get_input")
        self.get_input_proxy = rospy.ServiceProxy("/get_input", GetInput)

        communicator = RosCommunicator(
                self.get_input_proxy,
                self.print_output_publisher.publish
                )

        self.game = Game(communicator)


if __name__ == "__main__":
    node = DartNode()
    rospy.init_node("dart_node")
    node.game.run()
    rospy.spin()
