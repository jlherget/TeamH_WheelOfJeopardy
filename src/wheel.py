from enum     import Enum
from ui_utils import Colors

import pygame
import random
import math

class Section(Enum):
    """Define the wheel sections.

    This order aligns with the order in the wheel image.

    """
    CAT_6               = 11
    FREE_SPIN           = 10
    CAT_5               = 9
    LOSE_TURN           = 8
    CAT_4               = 7
    DOUBLE_SCORE        = 6
    CAT_3               = 5
    BANKRUPT            = 4
    CAT_2               = 3
    OPPONENT_CHOOSE_CAT = 2
    CAT_1               = 1
    CHOOSE_CAT          = 0

class Wheel():
    """The wheel will consist of various sections that define the player's turn.

    When triggered, the wheel will spin and produce an output. This output will be sent 
    to the WoJ for processing.

    """

    def __init__(self, app):
        self.app            = app                           # WoJ object
        self.ui             = WheelUI(self, app, 10, 60)    # User interface
        self.spinnable      = False                         # Flag to indicate the wheel is allowed to be spun
        self.angle          = 0                             # Current angle of the image                 | Deg, [0,360)
        self.angle_start    = 0                             # STarting angle of the image                | Deg, [0,360)
        self.angle_vel      = 0                             # Current angle velocity of the image        | Deg/s
        self.angle_vel_start= 0                             # Starting angle velocity of the image       | Deg/s
        self.angle_decel    = 0                             # How quickly to decelerate the wheel        | Deg/s^2
        self.start_spin_time= 0                             # Time wheel was last spun                   | ms, pygame time

    def enableSpin(self):
        """Allow the user to spin the wheel."""
        self.spinnable = True
    
    def disableSpin(self):
        """Prevent the wheel from spinning."""
        self.spinnable = False

    def Draw(self, screen):
        """Draw the wheel image onto the pygame screen object.

        Updates the wheel image angle based on time since it was last spun.
        If the wheel has just completed spinning send a result to the WojApp
        with the result of the wheel.

        """
        # If the wheel is spinning, update the image angle
        if self.angle_vel != 0:
            current_time = pygame.time.get_ticks()
            dt = (current_time - self.start_spin_time) / 1000 # Convert from ms to seconds

            # angular velocity (to detect when spinning has stopped)
            # w = alpha * dt   (w_0 is 0)
            self.angle_vel = self.angle_vel_start + self.angle_decel * dt

            # angular position
            # theta = theta_0 + w_0 * dt + alpha/2 * dt^2
            self.angle = self.angle_start + self.angle_vel_start * dt + (self.angle_decel/ 2) * dt**2
            self.angle %= 360 

            # Check if the wheel has stopped (i.e. velocity sign goes positive)
            if self.angle_vel >= 0:
                self.angle_vel = 0
                sector = math.floor(self.angle / (360 / 12))

                print("SPIN COMPLETED, SENDING SECTOR %i TO MAIN" % sector)
                section = Section(sector)
                self.app.wheelResult(section)

        # Actually draw the image.
        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        """Process user interface events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.Spin()

    def Spin(self):
        """Start spinning the wheel.
        
        Once the wheel has stopped spinning, it will send a message back to the WojApp object 
        indicating the result of spin.

        May only spin the wheel if it's not already spinning and spinning is enabled.

        """
        # Start spinning the wheel, if it's not already spinning and
        # we are allowed to spin it
        wheel_spin = pygame.mixer.Sound("resources/wheel.wav")
        wheel_spin.play()
        if self.spinnable == True and self.angle_vel == 0:
            self.start_spin_time  = pygame.time.get_ticks()
            self.angle_start      = self.angle
            self.angle_vel_start  = random.uniform(-700, -400)
            self.angle_vel        = self.angle_vel_start
            self.angle_decel      = random.uniform(140, 100)
            print("SPINNING WHEEL - VEL %f ACC %f" % (self.angle_vel, self.angle_decel))

class WheelUI():
    """Handles drawing the wheel image onto the pygame screen."""

    TRIANGLE_WIDTH  = 20
    TRIANGLE_HEIGHT = 15

    WHEEL_WIDTH     = 300
    WHEEL_HEIGHT    = 300
    WHEEL_SIZE      = (WHEEL_WIDTH, WHEEL_HEIGHT)

    def __init__(self, parent, app, pos_x, pos_y):
        self.parent          = parent
        self.app            = app
        self.pos_x          = pos_x
        self.pos_y          = pos_y
        self.wheel_img      = self.CreateWheelSurface()
        self.img_rect       = self.wheel_img.get_rect(topleft=(self.pos_x, self.pos_y))

    def CreateWheelSurface(self):
        """Load the wheel image into pygame."""
        wheel_img  = pygame.image.load("resources/wheel.png").convert_alpha()
        wheel_img  = pygame.transform.scale(wheel_img, self.WHEEL_SIZE)
        return wheel_img

    def Draw(self, screen):
        """Draw the wheel onto the screen.

        The wheel is a image loaded from a file rotated by some angle.

        """
        rot_image = pygame.transform.rotate(self.wheel_img, self.parent.angle)

        # Copy image to screen:
        self.img_rect = rot_image.get_rect(center=self.img_rect.center)
        screen.blit(rot_image, self.img_rect)

        # Draw little triangle at the top
        triangle_p1 = (self.pos_x + self.WHEEL_WIDTH / 2 - self.TRIANGLE_WIDTH / 2,
                       self.pos_y)
        triangle_p2 = (triangle_p1[0] + self.TRIANGLE_WIDTH / 2,
                       triangle_p1[1] + self.TRIANGLE_HEIGHT)
        triangle_p3 = (triangle_p1[0] + self.TRIANGLE_WIDTH, self.pos_y)
        triangle_points = [triangle_p1, triangle_p2, triangle_p3]

        pygame.draw.polygon(screen, Colors.GREEN, triangle_points)
