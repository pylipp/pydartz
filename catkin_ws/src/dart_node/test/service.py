#! /usr/bin/env python

from dart_node.srv import GetInput, GetInputResponse
import rospy


def handle_request(request):
    return GetInputResponse(raw_input(request.prompt))

if __name__ == "__main__":
    rospy.init_node("get_input_server")
    rospy.Service("/get_input", GetInput, handle_request)
    rospy.spin()
