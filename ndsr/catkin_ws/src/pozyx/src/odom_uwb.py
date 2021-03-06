#!/usr/bin/env python

# This node receive pose from UWB
# and transfer to the robot's frame
# then subtract with the last pose
# and get the difference to get the odometry measurement

import rospy
import rospkg
from geometry_msgs.msg import PoseStamped
import tf
import tf.transformations as tr
import numpy as np
import yaml

enable_filter = True
limit_speed = 5e-7 # mm/nsec

class odom_uwb(object):
    """docstring for odom_uwb."""
    def __init__(self):
        super(odom_uwb, self).__init__()

        # Read the config of the anchor node on the robot
        # should be a transformation matrix from the pose of the origin anchor node
        # to the origin of the robot
        self.config = self.load_config()

        self.pub_odom = rospy.Publisher("~odom", PoseStamped, queue_size=1)
        self.sub_pose = rospy.Subscriber("/pozyx_tag_node/pozyx_pose", PoseStamped, self.pose_callback, queue_size=1)

        self.previous_tf = None
        self.previous_time = rospy.Time()
        self.origin = []

    def pose_callback(self, msg):

        print "pose cb"
        trans = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]
        rot = [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]
        pose_matrix = tr.compose_matrix(angles = tr.euler_from_quaternion(rot), translate = trans)
        # Transfer to the frame of the robot
        # pose_matrix = np.dot(self.config, pose_matrix)

        if self.previous_tf is None: #if first callback
            odo_trans = trans
            odo_rot = rot
            odo = tr.compose_matrix(angles = tr.euler_from_quaternion(odo_rot), translate = odo_trans)

            self.origin = trans
        else:
            # calculate limit matrix
            if enable_filter:
                limit_dist = limit_speed * (msg.header.stamp.to_nsec() - self.previous_time.to_nsec())
                print (msg.header.stamp.to_nsec() - self.previous_time.to_nsec())
                scale, shear, angles, prev_trans, persp = tr.decompose_matrix(self.previous_tf)
                moved_vec = [msg.pose.position.x - prev_trans[0], 
                             msg.pose.position.y - prev_trans[1], 
                             msg.pose.position.z - prev_trans[2]]
                moved_dist = np.linalg.norm(moved_vec)
                if moved_dist > limit_dist:
                    #discard this pose
                    print "move too much"
                    return

            odo = np.dot(tr.inverse_matrix(self.previous_tf), pose_matrix)
            odo_trans = tf.transformations.translation_from_matrix(odo)
            odo_rot = tf.transformations.quaternion_from_matrix(odo)
        self.previous_time = msg.header.stamp
        self.previous_tf = pose_matrix

        print "x: ", trans[0]-self.origin[0], "y: ", trans[1]-self.origin[1], "z: ", trans[2]-self.origin[2]

        robot_odo = PoseStamped()
        robot_odo.header.stamp = msg.header.stamp
        robot_odo.pose.position.x = odo_trans[0]
        robot_odo.pose.position.y = odo_trans[1]
        robot_odo.pose.position.z = odo_trans[2]
        robot_odo.pose.orientation.x = odo_rot[0]
        robot_odo.pose.orientation.y = odo_rot[1]
        robot_odo.pose.orientation.z = odo_rot[2]
        robot_odo.pose.orientation.w = odo_rot[3]

        self.pub_odom.publish(robot_odo)

    def load_config(self):

        anchor_data = yaml.load(file(rospkg.RosPack().get_path('odom_uwb')+"/config/"+"husky.yaml",'r')) # Need RosPack get_path to find the file path
        trans = anchor_data['trans']
        rot = anchor_data['rot']

        return tr.compose_matrix(angles = rot, translate = trans)

if __name__ == '__main__':

    rospy.init_node('odom_uwb_node',anonymous=False)
    node = odom_uwb()
    rospy.spin()
