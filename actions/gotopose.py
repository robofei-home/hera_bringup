import actionlib
import rospy
import tf

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor

from hera.msg import gotoposeFeedback, gotoposeResult, gotoposeAction, gotoposeGoal

from move_base_msgs.msg import MoveBaseGoal
from geometry_msgs.msg import PoseStamped

class GotoPose(AbstractAction):
    """docstring for GotoPose."""
    def __init__(self, robot):
        super(GotoPose, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()

        self._as = actionlib.SimpleActionServer("gotopose", gotoposeAction, self.goal_callback, False)
        self._as.start()

        self.tf_listener = tf.TransformListener()

    def goal_callback(self, goal):
        result = self.execute(goal.location, goal.reference)
        self._as.set_succeeded(gotoposeResult(result=result))

    def execute(self, location, reference):
        self.robot.add_log('gotopose', '', color=LogColor.YELLOW)

        # get target position
        (target_trans, target_rot) = self.tf_listener.lookupTransform('/map', reference, rospy.Time(0))
        # (target_trans, target_rot) = get_tf(location)
        target = PoseStamped()
        target.header.frame_id = 'map'
        target.pose.position.x = target_trans[0] + location.position.x
        target.pose.position.y = target_trans[1] + location.position.y
        # target.pose.position.z = target_trans[2]
        # target.pose.orientation.x = target_rot[0]
        # target.pose.orientation.y = target_rot[1]
        target.pose.orientation.z = target_rot[2]
        target.pose.orientation.w = target_rot[3]
        
        # create goal
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = target.pose
        #
        return self.robot.get_actuators().goto(goal)