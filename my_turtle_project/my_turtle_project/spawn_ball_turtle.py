'''
this program is for spawning a turtle
'''

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn 

class TurtleSpawner(Node):
    def __init__(self):
        super().__init__('spawn_ball_turtle')
        self.cli = self.create_client(Spawn,'/spawn')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for /spawn service')
        self.req = Spawn.Request()
        self.req.x = 5.0
        self.req.y = 5.0
        self.req.theta = 0.0
        self.req.name = 'turtle2'
        self.future = self.cli.call_async(self.req)
    
def main(args =None):
        rclpy.init()
        node = TurtleSpawner()
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
     main()