#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState

import cv2
import mediapipe as mp


class HandGripperControl(Node):

    def __init__(self):
        super().__init__('hand_gripper_control')

        self.publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.cap = cv2.VideoCapture(0)  # safer default camera

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

        self.joint_names = [
            'front_left_wheel_joint',
            'front_right_wheel_joint',
            'back_left_wheel_joint',
            'back_right_wheel_joint',
            'arm_shoulder_pan_joint',
            'arm_shoulder_lift_joint',
            'arm_elbow_joint',
            'arm_wrist_1_joint',
            'arm_wrist_2_joint',
            'arm_wrist_3_joint',
            'gripper_robotiq_85_left_knuckle_joint',
            'gripper_robotiq_85_right_knuckle_joint',
            'gripper_robotiq_85_left_inner_knuckle_joint',
            'gripper_robotiq_85_right_inner_knuckle_joint',
            'gripper_robotiq_85_left_finger_tip_joint',
            'gripper_robotiq_85_right_finger_tip_joint'
        ]

        self.positions = [0.0] * len(self.joint_names)

        self.open_pos = 0.0
        self.closed_pos = 0.5

        self.last_state = "OPEN"

        self.get_logger().info("Hand gripper control started.")

    def finger_is_open(self, tip, pip):
        return tip.y < pip.y

    def detect_fist(self, landmarks):
        tips = [4, 8, 12, 16, 20]
        pips = [3, 6, 10, 14, 18]

        open_count = 0

        for t, p in zip(tips, pips):
            if self.finger_is_open(landmarks[t], landmarks[p]):
                open_count += 1

        return open_count == 0

    def set_gripper(self, value):
        # Main gripper joints
        self.positions[10] = value
        self.positions[11] = value

        # inner joints
        self.positions[12] = value
        self.positions[13] = value

        # finger tips
        self.positions[14] = value * 0.5
        self.positions[15] = value * 0.5

    def timer_callback(self):

        if not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                landmarks = hand_landmarks.landmark

                fist = self.detect_fist(landmarks)

                state = "CLOSE" if fist else "OPEN"

                if state != self.last_state:

                    if state == "CLOSE":
                        self.set_gripper(self.closed_pos)
                        self.get_logger().info("Gripper CLOSED")
                    else:
                        self.set_gripper(self.open_pos)
                        self.get_logger().info("Gripper OPEN")

                    self.last_state = state

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.positions

        self.publisher.publish(msg)

        cv2.imshow("Hand Gripper Control", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            self.cap.release()
            cv2.destroyAllWindows()


def main(args=None):
    rclpy.init(args=args)
    node = HandGripperControl()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()