import actionlib
import rospy
import tf

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor

from hera.msg import poseFeedback, poseResult, poseAction, poseGoal

from geometry_msgs.msg import PoseWithCovarianceStamped

class Pose(AbstractAction):
    """docstring for Pose."""
    def __init__(self, robot):
        super(Pose, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()

        self._as = actionlib.SimpleActionServer("pose", poseAction, self.goal_callback, False)
        self._as.start()

        self.tf_listener = tf.TransformListener()

    def goal_callback(self, goal):
        result = self.execute(goal.location)
        self._as.set_succeeded(poseResult(result=result))

    def execute(self, location):
        self.robot.add_log('Pose', location, color=LogColor.YELLOW)

        # get location tf
        (trans, rot) = self.tf_listener.lookupTransform('/map', location, rospy.Time(0))

        # create pose
        pose = PoseWithCovarianceStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = rospy.Time.now()
        pose.pose.pose.position.x = trans[0]
        pose.pose.pose.position.y = trans[1]
        pose.pose.pose.orientation.z = rot[2]
        pose.pose.pose.orientation.w = rot[3]

        # set pose
        self.robot.get_actuators().pose(pose)

        return 'success'
