import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class PickDemo(Node):
    def __init__(self):
        super().__init__('pick_demo')

        self.pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )

        self.timer = self.create_timer(2.0, self.run)

        self.done = False

    def run(self):
        if self.done:
            return

        msg = JointTrajectory()

        msg.joint_names = [
            'arm_shoulder_pan_joint',
            'arm_shoulder_lift_joint',
            'arm_elbow_joint',
            'arm_wrist_1_joint',
            'arm_wrist_2_joint',
            'arm_wrist_3_joint'
        ]

        point = JointTrajectoryPoint()

        # SIMPLE MOTION (just bends arm forward)
        point.positions = [0.0, -1.5, 1.5, -1.0, 1.5, 0.0]
        point.time_from_start.sec = 3

        msg.points.append(point)

        self.pub.publish(msg)

        self.get_logger().info("Moving arm...")

        self.done = True


def main():
    rclpy.init()
    node = PickDemo()
    rclpy.spin(node)

if __name__ == '__main__':
    main()