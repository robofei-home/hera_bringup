import actionlib
import rospy
import tf

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor

from hera.msg import headFeedback, headResult, headAction, headGoal

from std_msgs.msg import Float32MultiArray

class Head(AbstractAction):
    """docstring for Head."""
    def __init__(self, robot):
        super(Head, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()

        self._as = actionlib.SimpleActionServer("head", headAction, self.goal_callback, False)
        self._as.start()

        self.tf_listener = tf.TransformListener()

    def goal_callback(self, goal):
        result = self.execute(goal.pan.data, goal.tilt.data)
        self._as.set_succeeded(headResult(result=result))

    def execute(self, pan, tilt):
        self.robot.add_log('Head', str(pan)+" "+str(tilt), color=LogColor.YELLOW)

	goal = Float32MultiArray()

	goal.data = [pan,tilt]

        return self.robot.get_actuators().head(goal)

