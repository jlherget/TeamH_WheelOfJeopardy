import ui_utils
import pygame
import random
import math
import messages

class Wheel():

    WHEEL_SPIN_ACC          = 180

    def __init__(self, app):
        self.app            = app
        self.ui             = WheelUI(self, app, 10, 60)
        self.spinnable      = False
        self.angle          = 0
        self.angle_vel      = 0

    def enableSpin(self):
        self.spinnable = True
    
    def disableSpin(self):
        self.spinnable = False

    def Draw(self, screen):

         # If the wheel is spinning, update the image angle
        if self.angle_vel != 0:
            current_time = pygame.time.get_ticks()
            dt = (current_time - self.start_spin_time) / 1000 # Convert from ms to seconds

            # angular velocity (to detect when spinning has stopped)
            # w = alpha * dt   (w_0 is 0)
            self.angle_vel = self.angle_vel_start + self.angle_accel * dt #+ random.randrange(0, 1)/10000

            # angular position
            # theta = theta_0 + w_0 * dt + alpha/2 * dt^2
            self.angle = self.angle_start + self.angle_vel_start * dt + (self.angle_accel/ 2) * dt**2
            self.angle %= 360 

            # Check if the wheel has stopped (i.e. velocity sign goes positive)
            if self.angle_vel >= 0:
                self.angle_vel = 0
                sector = math.floor(self.angle / (360 / 12))

                print("SPIN COMPLETED, SENDING SECTOR %i TO MAIN" % sector)
                self.app.wheelResult(sector)

        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.Spin()

    def Spin(self):
        # Start spinning the wheel, if it's not already spinning and
        # we are allowed to spin it
        wheel_spin = pygame.mixer.Sound("resources/wheel.wav")
        wheel_spin.play()
        if self.spinnable == True and self.angle_vel == 0:
            self.start_spin_time  = pygame.time.get_ticks()
            self.angle_start      = self.angle
            self.angle_vel_start  = random.uniform(-700, -400)
            self.angle_vel        = self.angle_vel_start
            self.angle_accel      = random.uniform(140, 100)
            print("SPINNING WHEEL - VEL %f ACC %f" % (self.angle_vel, self.angle_accel))

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
