import math
from geometry_msgs.msg import TransformStamped, PoseStamped
import numpy as np
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster

class FramePublisher(Node):
    def __init__(self):
        super().__init__('goal_broadcaster')

        # Initialize the transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        
        self.subscription = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.handle_goal_2d,
            1)
        self.subscription # prevent unused variable warning
        self.timer = self.create_timer(0.1, self.broadcast_tf2)
        self.pos_and_orient = [None, None, None, None, None, None, None]

    def broadcast_tf2(self):
        if(self.pos_and_orient[0] == None):
            pass
        else:
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'world'
            t.child_frame_id = '2d_goal_tf'
            t.transform.translation.x = self.pos_and_orient[0]
            t.transform.translation.y = self.pos_and_orient[1]
            t.transform.translation.z = self.pos_and_orient[2]
            t.transform.rotation.x = self.pos_and_orient[3]
            t.transform.rotation.y = self.pos_and_orient[4]
            t.transform.rotation.z = self.pos_and_orient[5]
            t.transform.rotation.w = self.pos_and_orient[6]
            
            self.tf_broadcaster.sendTransform(t)

    def handle_goal_2d(self, msg):
        self.pos_and_orient[0] = msg.pose.position.x
        self.pos_and_orient[1] = msg.pose.position.y
        self.pos_and_orient[2] = msg.pose.position.z
        self.pos_and_orient[3] = msg.pose.orientation.x
        self.pos_and_orient[4] = msg.pose.orientation.y
        self.pos_and_orient[5] = msg.pose.orientation.z
        self.pos_and_orient[6] = msg.pose.orientation.w

def main():
    rclpy.init()
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()