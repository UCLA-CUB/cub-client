import sys
import vlc

from PyQt4.QtGui import *
from PyQt4.QtCore import *

FRONT = 0
REAR  = 1

camWins = [0, 0, 0]
frontCam = 0

# Handles instances of VLC media player
# Players can be created and recalled after a window has been closed
class MediaManager:

    instance = vlc.Instance()
    streamList = []
    IDs = []
    
    #def __init__(self, parent = None):
        #instance = vlc.Instance()

    def newPlayer (self, ID, path, volume):
        # VLC setup
        media = self.instance.media_new(path)
            
        # Initializing media player
        player = self.instance.media_player_new()
        player.set_media (media)
         
        player.audio_set_volume(volume) 
 
        self.streamList.append (player)
        self.IDs.append (ID)

        return player

    def getPlayer (self, ID):
        count = 0
        for s in self.IDs:                        

            if (s.capitalize == ID.capitalize):
                return self.streamList[count]
            count += 1
        
# Manages the Tiled Windows within the primary window.
class SubWindow(QWidget):
    def __init__(self, parent = None):
        super(SubWindow, self).__init__(parent)
                             
    def closeEvent(self, event):
        if (self.windowTitle == "Front Cam"):
            camWins[FRONT] = 1
        event.accept()

# Primary Window Setup.
class PrimaryWindow (QMainWindow):
    # Tracks the number of Sub Windows currently existing in the system.
    subCount = 0

    # Initiating the VLC Player Manager
    Media = MediaManager() 

    # Runs on boot.
    def __init__ (self, parent = None):
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
        print q.key()

        # Lookup table to connect keys to functions
        keys = {
            'X': self.close 
        }

        # Runs the function linked to the pressed key
        keys[(chr(q.key()) if q.key() < 256 else q.key())]()

    # Creates a new camera subwindow and links a VLC player to it.
    def newCamWindow (self, name, player):
        PrimaryWindow.subCount = PrimaryWindow.subCount+1
                
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
        
        #Sample for testing video streaming.
        path = "/home/greg/Downloads/Chevelle_The_Red.mp4"

        if q.text() == "Front":
            
            name = "Front Cam"
            camNum = FRONT

            if not (camWins[camNum]):
                # Initializing media player
                player = self.Media.newPlayer (name, path, 0)
                
                player.play()
                            
            if not (camWins[camNum] == 2):
                player = self.Media.getPlayer (name) 

                cam = self.newCamWindow(name, player)
                
                cam.show()                     
            
                camWins[camNum] = 2
        
        if q.text() == "Rear":
            name = "Rear Cam"
            camNum = REAR

            if not (camWins[camNum]):
                # Initializing media player
                player = self.Media.newPlayer (name, path, 0)
                
                player.play()
                            
            if not (camWins[camNum] == 2):
                player = self.Media.getPlayer (name) 

                cam = self.newCamWindow(name, player)
                
                cam.show()                     
            
                camWins[camNum] = 2


def main():
    # Create the Qt app object.
    app = QApplication(sys.argv)

    # QWidget is the base class of all user interface objects in PyQt4.
    ex = PrimaryWindow()
    
    # Show window after all setups are complete.
    ex.show ()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
