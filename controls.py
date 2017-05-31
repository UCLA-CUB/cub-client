import pygame
import client_interface

NUM_BUTTONS = 10

trigger_button = 1
camera_speed_mult = 0.002

pygame.init()

screen = pygame.display.set_mode((1,1))
pygame.display.quit()

# Manages linkage between the Controller and the Vehicle
class Driver:
    def __init__(self, host, port):
        self.buttonHistory = [0]*NUM_BUTTONS
        self.valid_controller = False

        pygame.joystick.init()
        self.interface = client_interface.ClientInterface(host, port)
        joystick_count = pygame.joystick.get_count() 

        for i in range(joystick_count):

            self.joystick = pygame.joystick.Joystick(i)
            self.joystick.init()

            if self.joystick.get_name() == "Microsoft SideWinder Precision 2 Joystick":
                print "Found a Microsoft SideWinder Precision 2 Joystick"
                self.buttonHistory[trigger_button] = self.joystick.get_button(trigger_button)
                self.valid_controller = True
                
                break

    def _isValid(self):
        return self.valid_controller
            
    def movementHandler(self):
        x_axis = self.joystick.get_axis(0)/2
        # The y axis is inverted on the joystick
        y_axis = -self.joystick.get_axis(1)/2 

        if not x_axis:
            return (0.5+y_axis, 0.5+y_axis)
        elif not y_axis:
            if x_axis > 0:
                return (0.5+x_axis, 0.5-x_axis)
            else:
                return (0.5+x_axis, 0.5-x_axis)
        else:
            return (0.5+(x_axis + y_axis)/2, 0.5+(-x_axis + y_axis)/2)

    def headlightsHandler(self):
        last_mode = self.joystick.get_button(trigger_button)
        if (not last_mode == self.buttonHistory[trigger_button]) and last_mode:
            self.buttonHistory[trigger_button] = last_mode
            return not self.interface.getHeadlights()
        else:
            self.buttonHistory[trigger_button] = last_mode
            return self.interface.getHeadlights()
        
    def cameraHandler(self):
        # Read in old values
        last_pos = self.interface.getCameraPos()
        joy_hat = self.joystick.get_hat(0)
        
        positions = list(last_pos)

        # Update to new values
        positions[0] = last_pos[0] + joy_hat[0] * camera_speed_mult
        positions[1] = last_pos[1] + joy_hat[1] * camera_speed_mult

        if positions[0] >= 1.0:
            positions[0] = 1.0

        if positions[1] >= 1.0:
            positions[1] = 1.0

        last_pos = positions

        return last_pos

    def updateValues(self):
        pygame.event.pump()

        move = self.movementHandler()
        headlight = self.headlightsHandler()
        cam  = self.cameraHandler()
        if (not move == getWheelSpeed()) or (not cam == getCameraPos()) or (not headlight == self.interface.getHeadlights()):
            self.interface.setWheelSpeed(move[0], move[1])
            self.interface.setHeadlights(headlight)
            self.interface.setCameraPos(cam[0], cam[1])
        
            self.interface.updateControl()

            print self.interface.getWheelSpeed()
            print self.interface.getHeadlights()
            print self.interface.getCameraPos()
        

