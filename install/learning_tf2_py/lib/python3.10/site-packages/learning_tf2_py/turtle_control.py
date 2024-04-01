import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Twist, PoseStamped, Quaternion
from turtlesim.srv import Spawn

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from turtlesim.msg import Pose
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        self.declare_parameter('turtle_frame', 'turtle1')
        self.turtle_frame = self.get_parameter('turtle_frame').get_parameter_value().string_value

        self.spawner = self.create_client(Spawn, 'spawn')

        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', QoSProfile(depth=10))

        self.timer = self.create_timer(1.0, self.on_timer)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.broadcaster = TransformBroadcaster(self)

        self.pose_subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.turtle_pose_callback,
            10)

    def turtle_pose_callback(self, msg):

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.turtle_frame
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0

        # Convert the Euler angle to a quaternion
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(msg.theta / 2.0)
        q.w = math.cos(msg.theta / 2.0)

        t.transform.rotation = q

        self.broadcaster.sendTransform(t)
    
    def on_timer(self):

        try:
            t = self.tf_buffer.lookup_transform('turtle1', '2d_goal_tf', rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(f'Could not transform turtle1 to 2d_goal_pose: {ex}')
            return

        msg = Twist()
        scale_rotation_rate = 1.0
        msg.angular.z = scale_rotation_rate * math.atan2(
            t.transform.translation.y,
            t.transform.translation.x)

        scale_forward_speed = 0.5
        msg.linear.x = scale_forward_speed * math.sqrt(
            t.transform.translation.x ** 2 +
            t.transform.translation.y ** 2)

        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    controller = TurtleController()

    rclpy.spin(controller)

    controller.destroy_node()
    rclpy.shutdown()
