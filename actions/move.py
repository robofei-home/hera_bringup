import actionlib
import rospy
import math
import time
import tf

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor
from agent.util.enuns import Side

from hera.msg import moveFeedback, moveResult, moveAction, moveGoal

from geometry_msgs.msg import Twist

class Move(AbstractAction):
    def __init__(self, robot):
        super(Move, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()

        self._as = actionlib.SimpleActionServer("move", moveAction, self.goal_callback, False)
        self._as.start()

    def goal_callback(self, goal):
        result = self.execute(goal.cmd, goal.vel, goal.seconds)
        self._as.set_succeeded(moveResult(result=result))

    def execute(self, cmd, vel, seconds):

        msg = Twist()
        if(cmd == 'up_left'):
            msg.linear.x = vel
            msg.linear.y = vel
        elif(cmd == 'spin_left_front'):
            msg.linear.x = vel
            msg.angular.z = vel
        elif(cmd == 'foward'):
            msg.linear.x = vel
        elif(cmd == 'spin_right_front'):
            msg.linear.x = vel
            msg.angular.z = -vel
        elif(cmd == 'up_right'):
            msg.linear.x = vel
            msg.linear.y = -vel
        elif(cmd == 'left'):
            msg.linear.y = vel
        elif(cmd == 'spin_left'):
            msg.angular.z = vel
        elif(cmd == 'spin_right'):
            msg.angular.z = -vel
        elif(cmd == 'right'):
            msg.linear.y = -vel
        elif(cmd == 'down_left'):
            msg.linear.x = -vel
            msg.linear.y = vel
        elif(cmd == 'spin_left_back'):
            msg.linear.x = -vel
            msg.angular.z = -vel
        elif(cmd == 'backward'):
            msg.linear.x = -vel
        elif(cmd == 'spin_right_back'):
            msg.linear.x = -vel
            msg.angular.z = vel
        elif(cmd == 'down_right'):
            msg.linear.x = -vel
            msg.linear.y = -vel
	elif(cmd == 'stop'):
            msg.linear.x = vel - vel
            msg.linear.y = vel - vel
            #msg.angular.z = 0

        self.robot.get_actuators().move(msg)

        if(seconds > 0):
            time.sleep(seconds)
            msg.linear.x = 0.0
            msg.linear.y = 0.0
            msg.linear.z = 0.0
            self.robot.get_actuators().move(msg)


    # def execute(self, type1, type2, direction, units, vel):
    #
    #     if(type1=='direction'):
    #         if(type2=='space'):
    #             initial_position = self.robot.get_sensors('odom').pose.pose.position
    #             while True:
    #                 self.direction(direction, vel)
    #                 actual_position = self.robot.get_sensors('odom').pose.pose.position
    #                 dist = math.sqrt(
    #                     (initial_position.x-actual_position.x)**2 +
    #                     (initial_position.y-actual_position.y)**2)
    #                 if (dist > units):
    #                     self.stop()
    #                     break
    #         elif(type2=='time'):
    #             start = time.time()
    #             done = time.time()
    #             elapsed = done - start
    #             while (elapsed < units):
    #                 done = time.time()
    #                 elapsed = done - start
    #                 self.direction(direction, vel)
    #             self.stop()
    #     if(type1=='spin'):
    #         if(type2=='space'):
    #             tolerance=math.radians(5)
    #             orientation = self.robot.get_sensors('odom').pose.pose.orientation
    #             quaternion = (
    #                 orientation.x,
    #                 orientation.y,
    #                 orientation.z,
    #                 orientation.w
    #             )
    #
    #             (x, y, z) = tf.transformations.euler_from_quaternion(quaternion)
    #             initial_angle = math.degrees(z)
    #
    #             while True:
    #                 orientation = self.robot.get_sensors('odom').pose.pose.orientation
    #                 quaternion = (
    #                     orientation.x,
    #                     orientation.y,
    #                     orientation.z,
    #                     orientation.w
    #                 )
    #
    #                 (x, y, z) = tf.transformations.euler_from_quaternion(quaternion)
    #                 actual_angle = math.degrees(z)
    #
    #                 dif = initial_angle - actual_angle
    #
    #                 if (dif > 180):
    #                     dif = dif - 360
    #                 if (dif < -180):
    #                     dif = dif + 360
    #
    #                 if (dif > math.degrees(-direction + tolerance)):
    #                     self.spin(Side.RIGHT.value, vel)
    #                 elif (dif < math.degrees(-direction - tolerance)):
    #                     self.spin(Side.LEFT.value, vel)
    #                 else:
    #                     self.stop()
    #                     break
    #
    #         elif(type2=='time'):
    #             self.spin(direction, vel)
    #             time.sleep(units)
    #             self.stop()
    #
    # def direction(self, direction, vel):
    #     msg = Twist()
    #     msg.linear.x = math.cos(direction) * vel
    #     msg.linear.y = math.sin(direction) * vel
    #     self.robot.get_actuators().move(msg)
    #
    # def spin(self, direction, vel):
    #     msg = Twist()
    #     msg.angular.z = vel * direction
    #     self.robot.get_actuators().move(msg)
    #
    # def stop(self):
    #     msg = Twist()
    #     self.robot.get_actuators().move(msg)
