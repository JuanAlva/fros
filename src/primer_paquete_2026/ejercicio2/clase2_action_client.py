#!/usr/bin/env python3
import time

import rclpy
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from std_msgs.msg import String

from primer_paquete_2026.action import MyAction


class TextActionClient(Node):

    def __init__(self):
        super().__init__('clase2_action_client')

        self.declare_parameter('text', 'Hola mundo desde ROS 2')
        self.text = self.get_parameter('text').get_parameter_value().string_value

        self.publisher_ = self.create_publisher(String, 'texto_republicado', 10)
        self._action_client = ActionClient(self, MyAction, 'repeat_text')

        self.send_goal()

    def send_goal(self):
        self.get_logger().info(f'Waiting for action server, will send: "{self.text}"')
        self._action_client.wait_for_server()

        goal_msg = MyAction.Goal()
        goal_msg.mytext = self.text

        send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback received: {feedback_msg.feedback.words}')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        if result.result:
            msg = String()
            msg.data = 'Texto republicado!'
            self.publisher_.publish(msg)
            self.get_logger().info(msg.data)

        time.sleep(0.5)
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = TextActionClient()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
