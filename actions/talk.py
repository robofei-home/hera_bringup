import actionlib
import rospy

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor

from hera.msg import talkFeedback, talkResult, talkAction, talkGoal

from gtts_ros.msg import TalkGoal
from std_msgs.msg import String

class Talk(AbstractAction):
    """docstring for Talk."""
    def __init__(self, robot):
        super(Talk, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()

        self._as = actionlib.SimpleActionServer("talk", talkAction, self.goal_callback, False)
        self._as.start()

        self.pub_vizbox_robot = rospy.Publisher('/robot_text', String, queue_size=80)

    def goal_callback(self, goal):
        result = self.execute(goal.phrase)
        self._as.set_succeeded(talkResult(result=result))

    def execute(self, phrase):
        ''' Execute action talk(phrase) '''
        self.robot.add_log('Talk', phrase, color=LogColor.CYAN)
        self.pub_vizbox_robot.publish(phrase)

        # create goal
        goal = TalkGoal()
        # set goal
        goal.phrase = phrase
        # talk
        result = self.robot.get_actuators().talk(goal)
        return 'success'
