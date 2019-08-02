import ui_utils
import pygame
import random
import math
import messages

class Wheel():
    def __init__(self, app):
        self.running = True
        self.app     = app
        self.ui      = WheelUI(app, 10, 60)

    def PostMessage(self, message):
        self.app.queue.put(message)

    def Draw(self, screen):
        self.ui.Draw(screen)

    def ProcessUiEvent(self, event):
        self.ui.ProcessUiEvent(event)

    def Spin(self):
        self.ui.Spin()

class WheelUI():
    TRIANGLE_WIDTH  = 20
    TRIANGLE_HEIGHT = 15

    WHEEL_WIDTH  = 300
    WHEEL_HEIGHT = 300
    WHEEL_SIZE   = (WHEEL_WIDTH, WHEEL_HEIGHT)

    WHEEL_SPIN_ACC          = 0.02
    WHEEL_SPIN_ANG_VEL_INIT = -5

    def __init__(self, app, pos_x, pos_y):
        self.app            = app
        self.pos_x          = pos_x
        self.pos_y          = pos_y
        self.angle          = 0
        self.angle_vel      = 0
        self.angle_acc      = 0
        self.prev_angle_vel = 0
        self.wheel_img      = self.CreateWheelSurface()
        self.img_rect       = self.wheel_img.get_rect(topleft=(self.pos_x, self.pos_y))

    def CreateWheelSurface(self):
        wheel_img  = pygame.image.load("resources/wheel.png").convert_alpha()
        wheel_img  = pygame.transform.scale(wheel_img, self.WHEEL_SIZE)
        return wheel_img

    def Spin(self):
        # Start spinning the wheel (if it's not already spinning)
        if self.angle_vel == 0:
            self.angle_vel = random.randrange(-10, -6)

    def Draw(self, screen):
        # If the wheel is spinning, update the image angle
        if self.angle_vel != 0:
            self.angle           += self.angle_vel
            self.prev_angle_vel   = self.angle_vel
            self.angle_vel       += self.WHEEL_SPIN_ACC + random.randrange(0, 1)/10000

            # Check if the wheel has stopped (i.e. velocity sign changes)
            if self.angle_vel == 0 or math.copysign(self.angle_vel, self.prev_angle_vel) != self.angle_vel:
                # At this point, we would send a message back to the app
                # with the result.
                self.angle_vel = 0

                print("SPIN COMPLETED, SENDING OUTPUT TO MAIN")
                sector = math.floor(self.angle / (360 / 2)) + 6
                self.app.PostMessage(messages.SpinOutMessage(sector))
            self.angle %= 360

        rot_image = pygame.transform.rotate(self.wheel_img, self.angle)

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

    def ProcessUiEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.app.wheelTurn:
                    self.app.PostMessage(messages.SpinInMessage())
                    self.Spin()



#todo
#build wheel, reset wheel, delete wheel
#SPIN THE WHEEL
