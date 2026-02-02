import rclpy 
from rclpy.node import Node 
from turtlesim.srv import TeleportAbsolute

class TurtlePlayer_1(Node):
    def __init__(self):
        super().__init__('turtle_player_1')

        # teleport the turtle to the bottom
        client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute') 
        while not client.wait_for_service(timeout_sec=1.0): 
            self.get_logger().info('waiting for teleport service...') 

        req = TeleportAbsolute.Request() 
        req.x = 5.0 
        req.y = 1.0 
        req.theta = 0.0

        self.future = client.call_async(req)
        self.get_logger().info("Teleport request sent to move turtle1 to bottom.")

def main(args=None):
    rclpy.init()
    node = TurtlePlayer_1()
    rclpy.spin(node)   # keep node alive so teleport request completes
    rclpy.shutdown()

if __name__ == "__main__":
    main()
