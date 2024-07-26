import sys
import threading
import pygame
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from pygame.locals import *

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Initialize the joystick
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

my_square = pygame.Rect(50, 50, 50, 50)
my_square_color = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
motion = [0, 0]

G = 180
L = 0

increment_running = False
decrement_running = False
increment_running2 = False
decrement_running2 = False

MAX_G = 180
MIN_G = 0
MAX_L = 180
MIN_L = 0

class ROSPublisher(Node):
    def __init__(self):
        super().__init__('joystick_publisher')
        self.publisher_ = self.create_publisher(String, 'joystick_topic', 10)

    def publish_message(self, message):
        msg = String()
        msg.data = message
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')

rclpy.init(args=None)
node = ROSPublisher()

def increment_G():
    global G
    while increment_running:
        if G < MAX_G:
            G += 1
        time.sleep(0.005)  # 50 milliseconds
        node.publish_message(f"Right {G}")
        print("Right", G)
        
def decrement_G():
    global G
    while decrement_running:
        if G > MIN_G:
            G -= 1
        time.sleep(0.005)  # 50 milliseconds
        node.publish_message(f"Right {G}")
        print("Right", G)

def increment_L():
    global L
    while increment_running2:
        if L < MAX_L:
            L += 1
        time.sleep(0.005)  # 50 milliseconds
        node.publish_message(f"Left {L}")
        print("Left", L)
        
def decrement_L():
    global L
    while decrement_running2:
        if L > MIN_L:
            L -= 1
        time.sleep(0.005)  # 50 milliseconds
        node.publish_message(f"Left {L}")
        print("Left", L)

def on_press(event):
    global increment_running
    increment_running = True
    thread = threading.Thread(target=increment_G)
    thread.start()

def on_press2(event):
    global decrement_running
    decrement_running = True
    thread = threading.Thread(target=decrement_G)
    thread.start()

def on_press3(event):
    global increment_running2
    increment_running2 = True
    thread = threading.Thread(target=increment_L)
    thread.start()

def on_press4(event):
    global decrement_running2
    decrement_running2 = True
    thread = threading.Thread(target=decrement_L)
    thread.start()

def on_release(event):
    global increment_running
    increment_running = False

def on_release2(event):
    global decrement_running
    decrement_running = False

def on_release3(event):
    global increment_running2
    increment_running2 = False

def on_release4(event):
    global decrement_running2
    decrement_running2 = False

def send_command(command):
    node.publish_message(command)
    time.sleep(0.1)

while True:
    if abs(motion[0]) < 0.1:
        motion[0] = 0
    if abs(motion[1]) < 0.1:
        motion[1] = 0
    my_square.x += motion[0] * 10
    my_square.y += motion[1] * 10

    for event in pygame.event.get():

        if event.type == JOYBUTTONDOWN:
            if event.button == 0:
                on_press2(event)
                my_square_color = (my_square_color + 1) % len(colors)

            elif event.button == 2:
                on_press(event)

            if event.button == 6:  # Button 6 pressed
                send_command("rightForward")
                print("rightForward")
            if event.button == 4:  # Button 4 pressed
                send_command("rightBackward")
                print("rightBackward")
            if event.button == 7:  # Button 7 pressed
                send_command("leftForward")
                print("leftForward")
            if event.button == 5:  # Button 5 pressed
                send_command("leftBackward")
                print("leftBackward")

        if event.type == JOYBUTTONUP:
            if event.button == 0:
                on_release(event)
            elif event.button == 2:
                on_release2(event)
            elif event.button == 6:  # Button 6 pressed
                send_command("stop")
                print("stop")
            elif event.button == 4:  # Button 4 pressed
                send_command("stop")
                print("stop")
            elif event.button == 7:  # Button 7 pressed
                send_command("stop")
                print("stop")
            elif event.button == 5:  # Button 5 pressed
                send_command("stop")
                print("stop")

            running = False
            increment_running = False
            decrement_running = False

        if event.type == JOYAXISMOTION:
            if event.axis == 1:
                if event.value == -1.000030518509476:
                    on_press3(event)
                elif event.value == -0.003936887722403638:
                    on_release4(event)
                    on_release3(event)
                elif event.value == 1.0:
                    on_press4(event)
            if event.axis < 2:
                motion[event.axis] = event.value
        if event.type == JOYHATMOTION:
            print(event)
        if event.type == JOYDEVICEADDED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for joystick in joysticks:
                print(joystick.get_name())
        if event.type == JOYDEVICEREMOVED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        if event.type == QUIT:
            pygame.quit()
            rclpy.shutdown()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                rclpy.shutdown()
                sys.exit()

    clock.tick(60)
