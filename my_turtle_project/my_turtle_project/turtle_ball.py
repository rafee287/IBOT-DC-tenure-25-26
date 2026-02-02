# import rclpy 
# from rclpy.node import Node 
# from geometry_msgs.msg import Twist
# import random
# from turtlesim.msg import Pose
# from turtlesim.srv import TeleportAbsolute
# import math 
# pie = math.pi
# class TurtleBall(Node):
#     def __init__(self):
#         super().__init__('turtle_ball')
#         self.pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
#         self.sub = self.create_subscription(Pose, '/turtle2/pose',self.change_dir,10)
#         self.sub2 = self.create_subscription(Pose,'/turtle3/pose',self.shot_2,10)
#         self.sub3 = self.create_subscription(Pose,'/turtle1/pose',self.shot_1,10)
#         # Rotate turtle2 to face northeast (x=5, y=5, theta=0.785 rad ~ 45°) 
#         self.client = self.create_client(TeleportAbsolute, '/turtle2/teleport_absolute') 
#         while not self.client.wait_for_service(timeout_sec=1.0): 
#             self.get_logger().info('waiting for teleport service...') 
#         req = TeleportAbsolute.Request() 
#         req.x = 5.0 
#         req.y = 5.0 
#         req.theta = random.random() *3.141592*2 
#         self.client.call_async(req)

#         self.twist = Twist()
#         self.twist.linear.x = 3.0
#         self.twist.angular.z = 0.0

#         # Set up a timer to publish continuously every 0.1 seconds
#         self.timer = self.create_timer(0.01, self.publish_cmd)

#         self.posball = None

#     def publish_cmd(self):
#         self.pub.publish(self.twist)
#         self.get_logger().info(
#             f"Publishing velocity: linear={self.twist.linear.x:.2f}, angular={self.twist.angular.z:.2f}"
#         )
    
#     def change_dir(self,msg:Pose):
        
#         self.posball = msg
#         req = TeleportAbsolute.Request()
#         if msg.x >= 10.5:
#             req.x = 10.4   # move slightly inside
#             req.y = msg.y
            
#             req.theta = pie - msg.theta
#             # req.theta = msg.theta + 1.570796
#             self.client.call_async(req)
#             self.get_logger().info(f"ball hit the right wall, going left")
#         elif msg.x <= 0.5:
#             req.x = 0.6    # move slightly inside
#             req.y = msg.y
#             req.theta = pie -msg.theta
#             # req.theta = msg.theta - 1.570796
#             self.client.call_async(req)
#             self.get_logger().info(f"ball hit the left wall, going right")            
#         elif msg.y>=10.5 or msg.y<=0.5:
#             req.x = 5.0
#             req.y = 5.0 
#             req.theta = random.random() *pie*2
#             self.client.call_async(req)
#             self.get_logger().info(f"ball missed, teleporting to the center")
    
#     # def shot_1(self,msg:Pose):
#     #     if self.posball is None: return
#     #     pos_player_1 = msg
#     #     req = TeleportAbsolute.Request()
#     #     if math.fabs(pos_player_1.x-self.posball.x) < 0.5 and math.fabs(pos_player_1.y-self.posball.y) < 0.5 :
#     #         req.x = self.posball.x
#     #         req.y = self.posball.y
#     #         req.theta = pie -msg.theta
#     #         self.client.call_async(req)
#     #         self.get_logger().info("Player 1 hit the ball!")
#     def shot_1(self, msg: Pose):
#         if self.posball is None:
#             return
#         if abs(msg.x - self.posball.x) < 0.5 and abs(msg.y - self.posball.y) < 0.5:
#             now = self.get_clock().now()
#             if (now - getattr(self, "last_hit_time1", now)).nanoseconds > 1e9:
#                 req = TeleportAbsolute.Request()
#                 #req.x = self.posball.x + 0.2
#                 req.x = self.posball.x + (0.3 if msg.x < self.posball.x else -0.3)
#                 req.y = self.posball.y
#                 req.theta = (pie - self.posball.theta)
#                 self.client.call_async(req)
#                 self.get_logger().info("Player 1 hit the ball!")
#                 self.last_hit_time1 = now


#     # def shot_2(self,msg:Pose):
#     #     if self.posball is None: return
#     #     pos_player_2 = msg
#     #     req = TeleportAbsolute.Request()
#     #     if math.fabs(pos_player_2.x-self.posball.x) < 0.5 and math.fabs(pos_player_2.y-self.posball.y) < 0.25 :
#     #         req.x = self.posball.x
#     #         req.y = self.posball.y
#     #         req.theta = pie-msg.theta
#     #         self.client.call_async(req)
#     #         self.get_logger().info("Player 2 hit the ball!")
#     def shot_2(self, msg: Pose):
#         if self.posball is None:
#             return
#         if abs(msg.x - self.posball.x) < 1.0 and abs(msg.y - self.posball.y) < 1.0:
#             now = self.get_clock().now()
#             if (now - getattr(self, "last_hit_time2", now)).nanoseconds > 1e9:
#                 req = TeleportAbsolute.Request()
#                 # req.x = self.posball.x + 0.2
#                 req.x = self.posball.x + (0.3 if msg.x < self.posball.x else -0.3)
#                 req.y = self.posball.y
#                 req.theta = (pie - self.posball.theta)
#                 self.client.call_async(req)
#                 self.get_logger().info("Player 2 hit the ball!")
#                 self.last_hit_time2 = now


# def main(args=None):
#     rclpy.init()
#     node = TurtleBall()
#     rclpy.spin(node)   # keep node alive, publishing continuously
#     rclpy.shutdown()

# if __name__ == "__main__":
#     main()


import rclpy 
from rclpy.node import Node 
from geometry_msgs.msg import Twist
import random
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute
import math 

pie = math.pi

class TurtleBall(Node):
    def __init__(self):
        super().__init__('turtle_ball')
        self.pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle2/pose', self.change_dir, 10)
        self.sub2 = self.create_subscription(Pose, '/turtle3/pose', self.shot_2, 10)
        self.sub3 = self.create_subscription(Pose, '/turtle1/pose', self.shot_1, 10)

        # Teleport client
        self.client = self.create_client(TeleportAbsolute, '/turtle2/teleport_absolute') 
        while not self.client.wait_for_service(timeout_sec=1.0): 
            self.get_logger().info('waiting for teleport service...') 

        # Start ball in center with random angle
        req = TeleportAbsolute.Request() 
        req.x = 5.0 
        req.y = 5.0 
        req.theta = random.random() * 2 * pie
        self.client.call_async(req)

        # Ball velocity
        self.twist = Twist()
        self.twist.linear.x = 2.0   # slightly slower for reliable collisions
        self.twist.angular.z = 0.0

        # Update at 100 Hz
        self.timer = self.create_timer(0.01, self.publish_cmd)

        self.posball = None
        self.last_hit_time1 = self.get_clock().now()
        self.last_hit_time2 = self.get_clock().now()

    def publish_cmd(self):
        self.pub.publish(self.twist)

    def change_dir(self, msg: Pose):
        self.posball = msg
        req = TeleportAbsolute.Request()

        if msg.x >= 10.5:
            req.x = 10.4
            req.y = msg.y
            req.theta = pie - msg.theta
            self.client.call_async(req)
            self.get_logger().info("Ball hit right wall, bouncing left")

        elif msg.x <= 0.5:
            req.x = 0.6
            req.y = msg.y
            req.theta = pie - msg.theta
            self.client.call_async(req)
            self.get_logger().info("Ball hit left wall, bouncing right")

        elif msg.y >= 10.5 or msg.y <= 0.5:
            req.x = 5.0
            req.y = 5.0
            req.theta = random.random() * 2 * pie
            self.client.call_async(req)
            self.get_logger().info("Ball missed, reset to center")

    def shot_1(self, msg: Pose):
        if self.posball is None:
            return
        if abs(msg.x - self.posball.x) < 1.0 and abs(msg.y - self.posball.y) < 0.5:
            now = self.get_clock().now()
            if (now - self.last_hit_time1).nanoseconds > 5e8:  # 0.5s cooldown
                req = TeleportAbsolute.Request()
                req.x = self.posball.x
                req.y = self.posball.y
                req.theta = (-self.posball.theta) % (2 * pie)
                self.client.call_async(req)

                # # reset velocity so ball moves in new direction
                # self.twist.linear.x = 2.0
                # self.twist.angular.z = 0.0

                self.get_logger().info("Player 1 hit the ball!")
                self.last_hit_time1 = now

    def shot_2(self, msg: Pose):
        if self.posball is None:
            return
        if abs(msg.x - self.posball.x) < 1.0 and abs(msg.y - self.posball.y) < 0.5:
            now = self.get_clock().now()
            if (now - self.last_hit_time2).nanoseconds > 5e8:  # 0.5s cooldown
                req = TeleportAbsolute.Request()
                req.x = self.posball.x
                req.y = self.posball.y
                req.theta = (-self.posball.theta) % (2 * pie)
                self.client.call_async(req)

                # # reset velocity so ball moves in new direction
                # self.twist.linear.x = 2.0
                # self.twist.angular.z = 0.0

                self.get_logger().info("Player 2 hit the ball!")
                self.last_hit_time2 = now

def main(args=None):
    rclpy.init()
    node = TurtleBall()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
