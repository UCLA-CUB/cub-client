import sys
import mediamanager
import controls
import threading
import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

CONTROLLER_HOST = "192.168.42.1"
CONTROLLER_PORT = 1337

address_front_cam = "http://88.53.197.250:80/axis-cgi/mjpg/video.cgi?resolution=320x240"
address_rear_cam = "http://195.235.198.107:3346/axis-cgi/mjpg/video.cgi?resolution=320x240"

front_cam_id = "FRONT_CAM"
rear_cam_id  = "REAR_CAM"

# Window Object for displaying video streams.
class MediaWindow (QWidget):
    def __init__ (self, parent = None):
        
        super(MediaWindow, self).__init__()

        self.graphics = QGraphicsView()
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.graphics)

        self.setLayout(self.layout) 

    def setPlayer(self, player):
        self.hide()
        
        self.stream = player

        if sys.platform.startswith('linux'):            
            player.set_xwindow (self.winId())
        elif sys.platform == "win32":
            player.set_hwnd (self.winId())

        self.show()

# Primary Window Setup.
class PrimaryWindow (QMainWindow):
    
    # Runs on boot.
    def __init__ (self, parent = None):
        # Tracks the number of Sub Windows currently existing in the system.
        self.subCount = 0

        # Initiating the VLC Player Manager
        self.Media = mediamanager.MediaManager()

        # Initializing both streams
        self.Media.newPlayer (front_cam_id, address_front_cam, 0)
        self.Media.newPlayer (rear_cam_id, address_rear_cam, 0)

        super (PrimaryWindow, self).__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget (self.mdi)
        bar = self.menuBar()

        # Media = MediaManager()

        # View Menu Option
        #view = bar.addMenu ("View")
        #view.addAction ("Tile")
        #view.triggered[QAction].connect (self.viewFunc)

        self.setWindowTitle ("CUB Control")

        self.layout = QVBoxLayout()
        self.mdi.setLayout(self.layout)

        # Building the format of the Window.
        # **********************************
        # *                                *
        # *                                *
        # *                                *
        # *         Player Window          *
        # *                                *
        # *                                *
        # **********************************
        # *         Select Stream          *
        # **********************************
        # *                     *          *
        # *                     *          *
        # *                     *          *
        # *       Feed          *   Data   *
        # *                     *          *
        # *                     *          *
        # *                     *          *
        # **********************************
        
        self.topLayout = QHBoxLayout()
        self.botLayout = QHBoxLayout()
        self.layout.addLayout(self.topLayout)
        self.layout.addLayout(self.botLayout)

        # Setting up text boxes for info.
        self.feed = QTextEdit()
        self.feed.setReadOnly(True)
        self.dataWin = QTextEdit()
        self.dataWin.setReadOnly(True)

        # Adding the video stream box.
        self.mediaWin = MediaWindow()
        self.mediaWin.setStyleSheet("background-color: transparent")
        self.mediaLayout = QVBoxLayout()
        self.topLayout.addLayout(self.mediaLayout)
        self.mediaLayout.addWidget(self.mediaWin)
        # Adding function key info.
        self.function = QTextEdit()
        self.topLayout.addWidget(self.function)


        # Adding the Select Stream Bar.
        self.streamBar = QHBoxLayout()
        barLText = QLineEdit()
        barLText.setAlignment(Qt.AlignRight)
        barLText.setText("Front")
        barLText.setReadOnly(True)
        barLText.setStyleSheet("background-color: transparent")
        barRText = QLineEdit()
        barRText.setText("Back")
        barRText.setReadOnly(True) 
        barRText.setStyleSheet("background-color: transparent")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,1)
        self.slider.valueChanged.connect(self.sliderEvent)
        #self.slider.valueChanged(camWindows)
        self.mediaLayout.addLayout(self.streamBar)
        self.streamBar.addWidget(barLText)
        self.streamBar.addWidget(self.slider)
        self.streamBar.addWidget(barRText)

        # Adding the Feed Window.
        self.botLayout.addWidget(self.feed)
        # Adding the Data Window.
        self.botLayout.addWidget(self.dataWin)

        # Initialize with front camera.
        self.camWindows(0)

    # Manages resize events (maintains scalability of window).
    def resizeEvent (self, evt = None):
        self.mediaWin.setFixedHeight(self.mdi.height()*3/5)
        self.dataWin.setFixedWidth(self.mdi.width()*2/5)
        self.function.setFixedWidth(self.dataWin.width())
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

    # Initializes a VLC Media Player and creates a new window with the corresponding Title.
    def camWindows (self, camID):
        if camID == 0:
            # Grabbing media player
            player = self.Media.newPlayer (front_cam_id, address_front_cam, 0)
                                    
        elif camID == 1:
            # Grabbing media player
            player = self.Media.newPlayer (rear_cam_id, address_rear_cam, 0)
            
        player.play() 
    
        self.mediaWin.clearPlayer()
        self.mediaWin.setPlayer(player)  
    
    # Slider event that changes currently displayed stream.
    def sliderEvent (self):
        camID = self.slider.value()
        self.camWindows(camID)

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
