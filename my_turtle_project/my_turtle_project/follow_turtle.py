import rclpy 
from rclpy.node import Node 
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class TurtleFollower(Node):
    def __init__(self):
        super().__init__('turtle_follower')           # initialises the name of the node as 'turtle_follower' this is how it appears in the ros2 node list
        self.sub = self.create_subscription(Pose, '/turtle1/pose',self.listener_callback,10)
        self.pub = self.create_publisher(Twist,'/turtle2/cmd_vel',10)

    def listener_callback(self,msg):
        twist = Twist()
        # example : making turtle2 move forward proportional to turtle1's x position
        twist.linear.x = msg.x*0.1
        twist.angular.z = msg.theta*0.1
        self.pub.publish(twist)
    
def main(args = None):
        rclpy.init()
        node = TurtleFollower()
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
    main()

