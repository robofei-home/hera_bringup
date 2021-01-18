import actionlib
import rospy
import tf

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor

from hera.msg import savelocalFeedback, savelocalResult, savelocalAction, savelocalGoal

from geometry_msgs.msg import Pose

class SaveLocal(AbstractAction):
    """docstring for SaveLocal."""
    def __init__(self, robot):
        super(SaveLocal, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()
        self.listener = tf.TransformListener()

        self._as = actionlib.SimpleActionServer("savelocal", savelocalAction, self.goal_callback, False)
        self._as.start()


    def goal_callback(self, goal):
        result = self.execute(goal.location)
        self._as.set_succeeded(savelocalResult(result=result))

    def execute(self, location):
        self.robot.add_log('Save Local', location, color=LogColor.YELLOW)
        # pose = self.robot.get_sensors('odom').pose.pose

        (trans,rot) = self.listener.lookupTransform('/map', '/base_link', rospy.Time(0))

        # create pose
        pose = Pose()
        pose.position.x = trans[0]
        pose.position.y = trans[1]
        pose.orientation.z = rot[2]
        pose.orientation.w = rot[3]

        # set pose
        self.robot.get_actuators().savelocal(location, pose)

        return 'success'
