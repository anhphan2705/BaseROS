#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from msgs.msg import BoundingBoxes
from message_filters import ApproximateTimeSynchronizer, Subscriber


class BBoxOverlayNode(Node):
    def __init__(self):
        super().__init__('bbox_overlay_node')

        self.declare_parameter('image_topic', '/camera/rectified/split_0')
        self.declare_parameter('detection_topic', '/yolo/detections_0')
        self.declare_parameter('output_topic', '/camera/yolo_overlay')

        image_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        detection_topic = self.get_parameter('detection_topic').get_parameter_value().string_value
        output_topic = self.get_parameter('output_topic').get_parameter_value().string_value

        self.bridge = CvBridge()

        self.image_sub = Subscriber(self, Image, image_topic)
        self.detection_sub = Subscriber(self, BoundingBoxes, detection_topic)

        self.ts = ApproximateTimeSynchronizer([self.image_sub, self.detection_sub], queue_size=10, slop=0.5)
        self.ts.registerCallback(self.callback)

        self.image_pub = self.create_publisher(Image, output_topic, 10)

        self.get_logger().info("BBoxOverlayNode with ID and depth annotation started!")

    def callback(self, img_msg: Image, boxes_msg: BoundingBoxes):
        try:
            frame = self.bridge.imgmsg_to_cv2(img_msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"cv_bridge error: {e}")
            return

        for box in boxes_msg.boxes:
            x1, y1, x2, y2 = box.x_min, box.y_min, box.x_max, box.y_max
            
            label = f"ID: {box.class_name}:{box.id:02d}"

            # if box.id[i] >= 0:
            #     label += f" | oID: {box.class_name[i]}:{box.class_id[i]:02d}"

            # if box.classification_id[i] >= 0:
            #     label += f" | cID: {box.classification_id[i]}"

            # label += f" | Conf: {box.confidence_interval[i]:.2f}"

            # Append depth if available
            if hasattr(box, 'depth') and box.depth > 0:
                label += f' ({box.depth:.2f}m)'

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 1, lineType=cv2.LINE_AA)

        self.get_logger().debug(f"Overlaying {len(boxes_msg.boxes)} boxes on image")
        overlay_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        overlay_msg.header = img_msg.header
        self.image_pub.publish(overlay_msg)


def main(args=None):
    rclpy.init(args=args)
    node = BBoxOverlayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()