import ui_utils
import pygame
import random
import math
import messages

class Wheel():

    WHEEL_SPIN_ACC          = 0.02
    WHEEL_SPIN_ANG_VEL_INIT = -5

    def __init__(self, app):
        self.app            = app
        self.ui             = WheelUI(self, app, 10, 60)
        self.spinnable      = False
        self.angle          = 0
        self.angle_vel      = 0
        self.angle_acc      = 0
        self.prev_angle_vel = 0

    def enableSpin(self):
        self.spinnable = True
    
    def disableSpin(self):
        self.spinnable = False

    def Draw(self, screen):

         # If the wheel is spinning, update the image angle
        if self.angle_vel != 0:
            self.angle           += self.angle_vel
            self.prev_angle_vel   = self.angle_vel
            self.angle_vel       += self.WHEEL_SPIN_ACC + random.randrange(0, 1)/10000

            # Check if the wheel has stopped (i.e. velocity sign changes)
            if self.angle_vel == 0 or math.copysign(self.angle_vel, self.prev_angle_vel) != self.angle_vel:
                self.angle_vel = 0
                sector = math.floor(self.angle / (360 / 12))

                print("SPIN COMPLETED, SENDING SECTOR %i TO MAIN" % sector)
                self.app.wheelResult(sector)

            # Keep angle between 0 and 360
            self.angle %= 360

        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.Spin()

    def Spin(self):
        # Start spinning the wheel, if it's not already spinning and
        # we are allowed to spin it
        if self.spinnable == True and self.angle_vel == 0:
            print("SPINNING WHEEL")
            self.angle_vel = random.randrange(-10, -6)

class WheelUI():
    TRIANGLE_WIDTH  = 20
    TRIANGLE_HEIGHT = 15

    WHEEL_WIDTH  = 300
    WHEEL_HEIGHT = 300
    WHEEL_SIZE   = (WHEEL_WIDTH, WHEEL_HEIGHT)

    def __init__(self, parent, app, pos_x, pos_y):
        self.parent          = parent
        self.app            = app
        self.pos_x          = pos_x
        self.pos_y          = pos_y
        self.wheel_img      = self.CreateWheelSurface()
        self.img_rect       = self.wheel_img.get_rect(topleft=(self.pos_x, self.pos_y))

    def CreateWheelSurface(self):
        wheel_img  = pygame.image.load("resources/wheel.png").convert_alpha()
        wheel_img  = pygame.transform.scale(wheel_img, self.WHEEL_SIZE)
        return wheel_img

    def Draw(self, screen):

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

        pygame.draw.polygon(screen, ui_utils.GREEN, triangle_points)