import actionlib
import rospy
import tf

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor

from hera.msg import followFeedback, followResult, followAction, followGoal
from social_navigation.msg import GotoGoal

from move_base_msgs.msg import MoveBaseGoal
from geometry_msgs.msg import PoseStamped

class Follow(AbstractAction):
    """docstring for Follow."""
    def __init__(self, robot):
        super(Follow, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()

        self._as = actionlib.SimpleActionServer("follow", followAction, self.goal_callback, False)
        self._as.start()

        self.tf_listener = tf.TransformListener()

    def goal_callback(self, goal):
        result = self.execute(goal.location)
        self._as.set_succeeded(followResult(result=result))

    def execute(self, location):
        self.robot.add_log('Follow', location, color=LogColor.YELLOW)

        # # get target position
        # (target_trans, target_rot) = self.tf_listener.lookupTransform('/map', location, rospy.Time(0))
        # # (target_trans, target_rot) = get_tf(location)
        # target = PoseStamped()
        # target.header.frame_id = 'map'
        # target.pose.position.x = target_trans[0]
        # target.pose.position.y = target_trans[1]
        # # target.pose.position.z = target_trans[2]
        # # target.pose.orientation.x = target_rot[0]
        # # target.pose.orientation.y = target_rot[1]
        # target.pose.orientation.z = target_rot[2]
        # target.pose.orientation.w = target_rot[3]
        #
        # # create goal
        # goal = MoveBaseGoal()
        # goal.target_pose.header.frame_id = 'map'
        # goal.target_pose.header.stamp = rospy.Time.now()
        # goal.target_pose.pose = target.pose
        #
        # return self.robot.get_actuators().goto_location(goal)

        # create goal
        goal = GotoGoal()
        goal.target = location
        return self.robot.get_actuators().follow(goal)

    # def execute(self, target_name):
        # pass
    #     # now = time.strftime("%H:%M:%S", time.localtime(time.time()))
    #     # self.report.log.append('\\lbrack' + str(now) + '\\rbrack ~ Goto \\textcolor{YellowOrange}{'+ target_name + '}.')
    #     # rospy.loginfo('Goto: ' + colored(target_name, 'yellow'))
    #
    #     self.robot.add_log('Goto', target_name, color=LogColor.YELLOW)
    #
    #     # get robot tf
    #     (robot_trans, robot_rot) = tf_listener.lookupTransform('/map', self.robot_ns+'base_link', rospy.Time(0))
    #
    #     # (robot_trans, robot_rot) = get_tf('base_link')
    #     robot = PoseStamped()
    #     robot.header.frame_id = 'map'
    #     robot.pose.position.x = robot_trans[0]
    #     robot.pose.position.y = robot_trans[1]
    #     # robot.pose.position.z = robot_trans[2]
    #     # robot.pose.orientation.x = robot_rot[0]
    #     # robot.pose.orientation.y = robot_rot[1]
    #     robot.pose.orientation.z = robot_rot[2]
    #     robot.pose.orientation.w = robot_rot[3]
    #
    #     # get target position
    #     (target_trans, target_rot) = tf_listener.lookupTransform('/map', target_name, rospy.Time(0))
    #     # (target_trans, target_rot) = get_tf(target_name)
    #     target = PoseStamped()
    #     target.header.frame_id = 'map'
    #     target.pose.position.x = target_trans[0]
    #     target.pose.position.y = target_trans[1]
    #     # target.pose.position.z = target_trans[2]
    #     # target.pose.orientation.x = target_rot[0]
    #     # target.pose.orientation.y = target_rot[1]
    #     target.pose.orientation.z = target_rot[2]
    #     target.pose.orientation.w = target_rot[3]
    #
    #     # get path orientation
    #     # plan = self.srv_make_plan(robot, target, 0.1)
    #     # a = numpy.array([plan.plan.poses[1].pose.position.x,
    #     #                  plan.plan.poses[1].pose.position.y])
    #     # b = numpy.array([plan.plan.poses[0].pose.position.x,
    #     #                  plan.plan.poses[0].pose.position.y])
    #     # c = a-b
    #     # ang = numpy.arctan2(c[1], c[0])
    #
    #
    #     # create goal
    #     goal = MoveBaseGoal()
    #     goal.target_pose.header.frame_id = 'map'
    #
    #     # step 1: rotate to next plan position
    #     # self.dr_client.update_configuration({
    #     #     'xy_goal_tolerance':0.3,
    #     #     'yaw_goal_tolerance':math.pi/72})
    #     # goal.target_pose.header.stamp = rospy.Time.now()
    #     # goal.target_pose.pose.position.x = robot.pose.position.x
    #     # goal.target_pose.pose.position.y = robot.pose.position.y
    #     # goal.target_pose.pose.orientation.z = ang
    #     # goal.target_pose.pose.orientation.w = 1.0
    #     # result = ''
    #     # while(result is not 'SUCCEEDED'):
    #     #     rospy.loginfo("rotate to next plan position")
    #     #     result = self.actuators.goto_location(goal)
    #     # self.move_spin_degrees.execute(math.degrees(ang))
    #
    #     # step 2: go to target translation
    #     # self.dr_client.update_configuration({
    #     #     'xy_goal_tolerance':0.1,
    #     #     'yaw_goal_tolerance':math.pi})
    #     # goal.target_pose.header.stamp = rospy.Time.now()
    #     # goal.target_pose.pose = target.pose
    #     # result = ''
    #     # while(result is not 'SUCCEEDED'):
    #     #     rospy.loginfo("go to target twait_for_serverranslation")
    #     #     result = self.actuators.goto_location(goal)
    #
    #     # step 3: go to target rotation
    #     # self.dr_client.update_configuration({
    #     #     'xy_goal_tolerance':0.3,
    #     #     'yaw_goal_tolerance':math.pi/36})
    #     goal.target_pose.header.stamp = rospy.Time.now()
    #     goal.target_pose.pose = target.pose
    #     result = ''
    #     while(result is not 'SUCCEEDED'):
    #         result = self.robot.get_actuators().goto_location(goal)
