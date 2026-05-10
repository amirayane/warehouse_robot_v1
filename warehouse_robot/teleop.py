import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import sys, select, termios, tty
import time

msg = """
Control Your Robot:
---------------------------
W : forward
S : backward
A : turn left
D : turn right
SPACE : stop
CTRL+C : quit
"""

move_bindings = {
    'w': (0.2, 0.0),
    's': (-0.2, 0.0),
    'a': (0.0, 0.4),
    'd': (0.0, -0.4),
    ' ': (0.0, 0.0),
}

class Teleop(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')

        self.pub = self.create_publisher(
            TwistStamped,
            '/diff_drive_controller/cmd_vel',
            10
        )

        self.settings = termios.tcgetattr(sys.stdin)
        self.last_time = time.time()
        self.timeout = 0.5

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = sys.stdin.read(1) if rlist else ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run(self):
        print(msg)

        while rclpy.ok():
            key = self.get_key()

            cmd = TwistStamped()
            cmd.header.frame_id = "base_link"

            if key in move_bindings:
                linear, angular = move_bindings[key]
                cmd.twist.linear.x = float(linear)
                cmd.twist.angular.z = float(angular)
                self.last_time = time.time()

            else:
                # safety stop if no input for a while
                if time.time() - self.last_time > self.timeout:
                    cmd.twist.linear.x = 0.0
                    cmd.twist.angular.z = 0.0

            self.pub.publish(cmd)

            if key == '\x03':  # CTRL+C
                break


def main():
    rclpy.init()
    node = Teleop()

    try:
        node.run()
    except KeyboardInterrupt:
        pass

    # STOP robot before exit
    stop = TwistStamped()
    stop.header.frame_id = "base_link"
    stop.twist.linear.x = 0.0
    stop.twist.angular.z = 0.0
    node.pub.publish(stop)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()