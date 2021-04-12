import actionlib
import rospy

from agent.abstract_action import AbstractAction
from agent.util.enuns import LogColor

from hera.msg import hearFeedback, hearResult, hearAction, hearGoal

from gsr_ros.srv import Start, StartRequest
from gsr_ros.msg import Opcs
from std_msgs.msg import String

class Hear(AbstractAction):
    """docstring for Hear."""
    def __init__(self, robot):
        super(Hear, self).__init__(robot)
        self.robot_ns = rospy.get_namespace()

        self._as = actionlib.SimpleActionServer("hear", hearAction, self.goal_callback, False)
        self._as.start()

        self.pub_vizbox_operator = rospy.Publisher('/operator_text', String, queue_size=80)

    def goal_callback(self, goal):
        speech = self.execute(goal)
        self._as.set_succeeded(hearResult(result=speech.result, choices=speech.choices))


    def repeat(self, recognition):
        # recognition = speech.result
        # for i in speech.choices:
        #     recognition = recognition.replace('<'+i.id+'>', i.values[0], 1)

        if(recognition is not ''):
            robot.get_actuators().talk.execute("I hear: " + str(recognition))

    def confirm(self, recognition):
        # recognition = speech.result
        # for i in speech.choices:
        #     recognition = recognition.replace('<'+i.id+'>', i.values[0], 1)

        if(recognition is not ''):
            self.get_actuators().talk.execute('Did you say: ' + str(recognition))
            self.get_actuators().talk.execute('is that correct?')

            ans = self.execute(['yes','no'],[])
            if (ans.result == 'yes'):
                return True
            else:
                return False
        else:
            return False

    def execute(self, srv, ask_confirm=False, repeat=False):
        ''' wait recognition of spec list  '''

        self.robot.add_log('Waiting command', str(srv.spec), color=LogColor.CYAN)

        # srv = StartRequest()
        # srv.spec = spec
        # srv.choices = choices
        # # for x in choices:
        # #     o = Opcs()
        # #     o.id = x['id']
        # #     for y in x['values']:
        # #         o.values.append(y)
        # #     srv.choices.append(o)

        speech = self.robot.get_actuators().hear(srv.spec, srv.choices)
        recognition = speech.result
        for i in speech.choices:
            recognition = recognition.replace('<'+i.id+'>', i.values[0], 1)

        if(recognition is not ''):
            self.pub_vizbox_operator.publish(recognition)
            self.robot.add_log('Hear', recognition, color=LogColor.CYAN)

        if (repeat):
            self.repeat(recognition)

        if (ask_confirm and (self.confirm(recognition) == False)):
            speech.result = ''

        return speech
