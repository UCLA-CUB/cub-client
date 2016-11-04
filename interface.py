import sys
import vlc
import controls
import threading
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

CONTROLLER_HOST = "192.168.42.1"
CONTROLLER_PORT = 1337

PLAYER_VOLUME = 0

address_front_cam = "http://88.53.197.250:80/axis-cgi/mjpg/video.cgi?resolution=320x240"
address_rear_cam = "http://88.53.197.250:80/axis-cgi/mjpg/video.cgi?resolution=320x240"

# Handles instances of VLC media player
# Players can be created and recalled after a window has been closed
class MediaManager:
        
    def __init__(self, parent = None):
        self.instance = vlc.Instance()
        # Dict containing player instances
        self.streamList = {}
 
    def newPlayer (self, ID, path, volume):
        
        # If a player already exists with this ID, return it
        if self.streamList.get(ID.capitalize()):
            return self.streamList.get(ID.capitalize())

        # VLC setup
        media = self.instance.media_new(path)
            
        # Initializing new media player and adding to dict
        player = self.streamList[ID.capitalize()] = self.instance.media_player_new()
        player.set_media (media)
         
        player.audio_set_volume(PLAYER_VOLUME) 
        
        return player
        
# Manages the Tiled Windows within the primary window.
class SubWindow(QWidget):
    def __init__(self, parent = None):
        super(SubWindow, self).__init__(parent)

        graphicsView = QGraphicsView()
        graphicsView.setStyleSheet("border: 0px")

        grid = QGridLayout()
        grid.addWidget(graphicsView)

        self.setLayout(grid)

                                     
    def closeEvent(self, event):
        parent.self.windowTitle()
        event.accept()

# Primary Window Setup.
class PrimaryWindow (QMainWindow):
    
    # Runs on boot.
    def __init__ (self, parent = None):
        # Tracks the number of Sub Windows currently existing in the system.
        self.subCount = 0

        # Initiating the VLC Player Manager
        self.Media = MediaManager() 


        super (PrimaryWindow, self).__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget (self.mdi)
        bar = self.menuBar()

        # Media = MediaManager()

        # View Menu Option
        view = bar.addMenu ("View")
        view.addAction ("Tile")
        view.triggered[QAction].connect (self.viewFunc)

        # Camera dropdown menu management
        cams = view.addMenu ("Cams")
        cams.addAction ("Front")
        cams.addAction ("Rear")        
        cams.triggered[QAction].connect (self.camWindows)
        
        self.mdi.tileSubWindows()

        self.setWindowTitle ("CUB Control")

    # Tiles all windows
    def viewFunc (self, q):
        if q.text() == "Tile":
            self.mdi.tileSubWindows()
    
    # Manages key actions
    def keyPressEvent (self, q):
        # Uncomment to debug key numbers
        # print q.key()

        # Lookup table to connect keys to functions
        keys = {
            'X': self.close 
        }

        # Runs the function linked to the pressed key
        try:
            keys[(chr(q.key()) if q.key() < 256 else q.key())]()
        except:
            print

    # Creates a new camera subwindow and links a VLC player to it.
    def newCamWindow (self, name, player):
        self.subCount = self.subCount+1
                
        win = SubWindow()
        win.setMinimumSize (300,300)
        #front.setWidget (QTextEdit())
        win.setWindowTitle (name)
        self.mdi.addSubWindow(win) 
            
        # Linking VLC Player to Qt SubWindow
        newWin = int(win.winId())

        if sys.platform.startswith('linux'):            
            player.set_xwindow (newWin)
        elif sys.platform == "win32":
            player.set_hwnd (newWin)
            
        return win


    # Initializes a VLC Media Player and creates a new window with the corresponding Title.
    def camWindows (self, q):
        if q.text() == "Front":
            name = "Front Cam"

            # Initializing media player
            player = self.Media.newPlayer (name, address_front_cam, 0)
                
            player.play() 

            cam = self.newCamWindow(name, player)
                
            cam.show()                     
                    
        if q.text() == "Rear":
            name = "Rear Cam"
            camNum = REAR

            # Initializing media player
            player = self.Media.newPlayer (name, address_rear_cam, 0)
                
            player.play() 

            cam = self.newCamWindow(name, player)
                
            cam.show()                     

# This loop manages the controller updates.
def controllerLoop ():
    controller = controls.Driver(CONTROLLER_HOST, CONTROLLER_PORT)
    while controller._isValid():
        controller.updateValues()
        time.sleep(0.05)

    self._stop.set()
        
def main():

    run = True

    # Setup the control device.
    #controller_thread = StoppableThread(threading.Thread(target = controllerLoop).start())
    threading.Thread(target = controllerLoop).start()
    
    # controllerLoop();

    # Create the Qt app object.
    app = QApplication(sys.argv)

    # QWidget is the base class of all user interface objects in PyQt4.
    ex = PrimaryWindow()
    
    # Show window after all setups are complete.
    ex.show ()
    
    run = False

    time.sleep(2)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
