import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys
import threading
import pygame
import time
import serial  # Import the serial library
from pygame.locals import *

ser = serial.Serial('/dev/ttyACM0', 9600) 

def send_command(command):
    ser.write(command.encode() + b'\n')
    time.sleep(0.001)
    
class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'joystick_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        send_command(msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
