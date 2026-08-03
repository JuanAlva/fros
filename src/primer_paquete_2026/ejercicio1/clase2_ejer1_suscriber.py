#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from rclpy.executors import ExternalShutdownException

from std_srvs.srv import Trigger

class CounterSubscriber(Node):
    def __init__(self):
        super().__init__('counter_subscriber')
        self.subscription = self.create_subscription(
            Int32,
            'counter_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.declare_parameter('reset_value', 50)
        self.reset_value = self.get_parameter('reset_value').get_parameter_value().integer_value

        self.cli = self.create_client(Trigger, 'reset_counter')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')
        if msg.data >= self.reset_value:
            self.cli.call_async(Trigger.Request())

        

def main(args=None):
    rclpy.init(args=args)
    node = CounterSubscriber()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
