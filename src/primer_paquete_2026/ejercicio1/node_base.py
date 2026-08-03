import rclpy
from rclpy.node import Node

class CounterSubscriber(Node):
    def __init__(self):
        super().__init__('counter_subscriber')

def main(args=None):
    rclpy.init(args=args)
    node = CounterSubscriber()
    rclpy.spin(node)
    rclpy.try_shutdown()

if __name__ == '__main__':
    main()