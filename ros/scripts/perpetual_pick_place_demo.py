#!/usr/bin/env python
import rospy
from std_msgs.msg import String

class kinova_demo(object):
    def __init__(self):
        rospy.init_node('kinova_demo', anonymous=True, disable_signals=True)
        self.kinova_pub = rospy.Publisher('/pick_and_place/event_in', String, queue_size=1)
        self.perceive_pub = rospy.Publisher('/pcl_closest_obj/event_in', String, queue_size=1)
        self.event_out_sub = rospy.Subscriber('/pick_and_place/event_out', String, self.event_out_cb)
        self.feedback = None
        self.rate = rospy.Rate(1) # 10hz
        rospy.sleep(1)
        print ("[kinova demo ] Ready!")

    def event_out_cb(self, msg):
        if msg.data == 'e_done':
            self.feedback = 'e_done'


    def perceive(self, side='left'):
        print ("[kinova demo ] Perceive move arm")
        if 'left' == side:
            self.kinova_pub.publish('e_perceive_left')
        else:
            self.kinova_pub.publish('e_perceive_right')

        while not rospy.is_shutdown():
            if self.feedback == 'e_done':
                self.feedback = None
                break
            self.rate.sleep()
        print ("[kinova demo ] moved arm now perceive")
        self.perceive_pub.publish('e_start')
        rospy.sleep(5)
        print ("[kinova demo ] Perceived ")

    def pick(self, side='left'):
        print ("[kinova demo ] Pick")
        if 'left' == side:
            self.kinova_pub.publish('e_pick_left')
        else:
            self.kinova_pub.publish('e_pick_right')
        while not rospy.is_shutdown():
            if self.feedback == 'e_done':
                self.feedback = None
                break
            self.rate.sleep()
        print ("[kinova demo ] Completed Pick")
        self.kinova_pub.publish('e_demo')
        while not rospy.is_shutdown():
            if self.feedback == 'e_done':
                self.feedback = None
                break
            self.rate.sleep()


if __name__ == '__main__':
    kinova = kinova_demo()
    try:
        while True:
            kinova.perceive(side='left')
            kinova.pick(side='left')
            kinova.perceive(side='right')
            kinova.pick(side='right')
    except KeyboardInterrupt:
        print ('Keyboard Interrupt shutting down Bye!')
        pass
