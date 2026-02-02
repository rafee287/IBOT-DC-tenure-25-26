'''
this program is for spawning a turtle
'''

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn 

class SpawnPlayer2Turtle(Node):
    def __init__(self):
        super().__init__('spawn_player_2_turtle')
        self.cli = self.create_client(Spawn,'/spawn')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for /spawn service')
        self.req = Spawn.Request()
        self.req.x = 5.0
        self.req.y = 0.0
        self.req.theta = 0.0
        self.req.name = 'turtle3'
        self.future = self.cli.call_async(self.req)
        self.get_logger().info("Spawn player 2 turtle node started")
    
def main(args =None):
        rclpy.init()
        node = SpawnPlayer2Turtle()
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
     main()