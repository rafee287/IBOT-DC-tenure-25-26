# import rclpy 
# from rclpy.node import Node 
# from turtlesim.srv import TeleportAbsolute
# from geometry_msgs.msg import Twist 
# from turtlesim.msg import Pose
# import math

# class TurtlePlayer_2(Node):
#     def __init__(self):
#         super().__init__('turtle_player_2')

#         # self.pub = self.create_publisher(Twist,'/turtle3/cmd_vel',10)
#         self.sub = self.create_subscription(Pose,'/turtle2/pose',self.follow,10)
#         # teleport the turtle to the bottom
#         self.client = self.create_client(TeleportAbsolute, '/turtle3/teleport_absolute') 
#         while not self.client.wait_for_service(timeout_sec=1.0): 
#             self.get_logger().info('waiting for teleport service...') 

#         req = TeleportAbsolute.Request() 
#         req.x = 5.0 
#         req.y = 10.0 
#         req.theta = 0.0

#         self.client.call_async(req)
#         self.get_logger().info("Teleport request sent to move turtle1 to bottom.")

#         self.ball_pose = None


#     def follow(self,msg:Pose):
#         req = TeleportAbsolute.Request()
#         if msg.theta < math.pi/2:
#             req.x = msg.x + 0.5
#         else:
#             req.x = msg.x - 0.5
         
#         req.y = 10.0
#         req.theta = 0.0
#         self.client.call_async(req)
#         self.get_logger().info(f"Turtle3 teleported to x={msg.x:.2f}, y=10.0")



# def main(args=None):
#     rclpy.init()
#     node = TurtlePlayer_2()
#     rclpy.spin(node)   # keep node alive so teleport request completes
#     rclpy.shutdown()

# if __name__ == "__main__":
#     main()

import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute
from turtlesim.msg import Pose
import math

class TurtlePlayer_2(Node):
    def __init__(self):
        super().__init__('turtle_player_2')

        # Subscribe to ball (turtle2) pose
        self.sub = self.create_subscription(Pose, '/turtle2/pose', self.ball_callback, 10)

        # Teleport client for turtle3
        self.client = self.create_client(TeleportAbsolute, '/turtle3/teleport_absolute')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for teleport service...')

        # Teleport turtle3 to the top initially
        req = TeleportAbsolute.Request()
        req.x = 5.0
        req.y = 10.0
        req.theta = 0.0
        self.client.call_async(req)
        self.get_logger().info("Teleport request sent to move turtle3 to top.")

        # Store latest ball pose
        self.ball_pose = None

        # Timer to send teleport requests at fixed frequency (e.g. 20 Hz)
        self.timer = self.create_timer(0.01, self.follow_timer)

    def ball_callback(self, msg: Pose):
        # Just store the latest ball pose
        self.ball_pose = msg

    def follow_timer(self):
        if self.ball_pose is None:
            return

        # Use your original logic: offset based on ball angle
        req = TeleportAbsolute.Request()
        if self.ball_pose.theta < math.pi / 2:
            req.x = self.ball_pose.x + 0.5
        else:
            req.x = self.ball_pose.x - 0.5

        req.y = 10.0
        req.theta = 0.0
        self.client.call_async(req)
        self.get_logger().info(f"Turtle3 teleported to x={req.x:.2f}, y=10.0")

def main(args=None):
    rclpy.init()
    node = TurtlePlayer_2()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
