import vlc 

MEDIA_VOLUME = 0

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
         
        player.audio_set_volume(MEDIA_VOLUME) 
        
        return player
 
