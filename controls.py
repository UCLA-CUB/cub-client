import pygame

# Manages linkage between the Controller and the Vehicle
class Driver:
    def __init__:
        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):

            self.joystick = pygame.joystick.Joystick(i)

            if self.joystick.get_name() == "Microsoft SideWinder Precision 2 Joystick":
                break

        print "Got it"    
        
    def updateValues:



