import json
import socket

from util.control import ControlSocket

class ClientInterface(object):
    def __init__(self, host, port):
        self.camera_pos = (0.0, 0.0)
        self.wheel_speed = (0.0, 0.0)
        self.headlights = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.connect((host, port))

        self.cs = ControlSocket(self.socket)

        self.oldcontrol = {}

    def __del__(self):
        self.socket.close()

    def setCameraPos(self, x, y):
        self.camera_pos = (x, y)
    
    def getCameraPos(self):
        return self.camera_pos

    def setWheelSpeed(self, l, r):
        self.wheel_speed = (l, r)

    def getWheelSpeed(self):
        return self.wheel_speed

    def setHeadlights(self, h):
        self.headlights = h

    def getHeadlights(self):
        return self.headlights

    def updateControl(self):
        newcontrol = {"left_motor" : self.wheel_speed[0], "right_motor" : self.wheel_speed[1]}

        if self.oldcontrol != newcontrol:
            self.cs.transmitControl(newcontrol)
            self.oldcontrol = newcontrol
        
