#!/usr/bin/env python3
import time

import rclpy
from rclpy.action import ActionServer
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from primer_paquete_2026.action import MyAction


class TextActionServer(Node):

    def __init__(self):
        super().__init__('clase2_action_server')
        self._action_server = ActionServer(
            self,
            MyAction,
            'repeat_text',
            execute_callback=self.execute_callback,
        )

    def execute_callback(self, goal_handle):
        text = goal_handle.request.mytext
        self.get_logger().info(f'Goal received: "{text}"')

        feedback_msg = MyAction.Feedback()
        for word in text.split():
            feedback_msg.words = word
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {word}')
            time.sleep(1.0)

        goal_handle.succeed()

        result = MyAction.Result()
        result.result = True
        return result


def main(args=None):
    rclpy.init(args=args)
    node = TextActionServer()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
