#!/usr/bin/env python

from agent.abstract_agent import AbstractAgent

from hera.actions.face import Face
from hera.actions.goto import Goto
from hera.actions.gotopose import GotoPose
from hera.actions.hear import Hear
from hera.actions.move import Move
from hera.actions.pose import Pose
from hera.actions.talk import Talk
#from hera.actions.follow import Follow
from hera.actions.savelocal import SaveLocal
from hera.actions.head import Head

from hera.srv import question, questionResponse

import rospy
import json

class Robot(AbstractAgent):
    """docstring for Robot"""
    def __init__(self):
        """ init """
        rospy.init_node('Robot')
        super(Robot, self).__init__()

        ''' actions '''
        self.actions.add_action('face', Face(self))
        self.actions.add_action('goto', Goto(self))
	self.actions.add_action('gotopose', GotoPose(self))
        self.actions.add_action('hear', Hear(self))
        self.actions.add_action('move', Move(self))
        self.actions.add_action('pose', Pose(self))
        self.actions.add_action('talk', Talk(self))
#        self.actions.add_action('follow', Follow(self))
        self.actions.add_action('savelocal', SaveLocal(self))
        self.actions.add_action('head', Head(self))

        ''' services '''
        s = rospy.Service('question', question, self.handle_question)

    def cicle(self):
        pass

    def handle_question(self, req):
        if(req.question == 'know_places'):
            return questionResponse(json.dumps(self.get_sensors('locals').strings))
        if(req.question == 'nearest_person'):
            p = self.get_sensors('people').people
            if(len(p) > 0):
                return questionResponse(json.dumps(p[0].name))
            else:
                return questionResponse(json.dumps(None))
        if(req.question == 'is_front_free'):
            dist = 2.0
            alfa = 5
            half = len(self.get_sensors('scan').ranges) / 2

            min_dist = min(self.get_sensors('scan').ranges[int(half - alfa):int(half + alfa)])

            if min_dist >= dist:
                return questionResponse(json.dumps(True))
            else:
                return questionResponse(json.dumps(False))



if __name__ == '__main__':
    Robot()
