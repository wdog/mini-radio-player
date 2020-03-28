import vlc
import time
import logging 

class Player:

    current_station = None
    is_playing = False
    instance = None


    def __init__(self):
        try:
            self.instance = vlc.Instance('--verbose=-1')
            self.player = self.instance.media_player_new()
            # add avent for tittle change
            self.events = self.player.event_manager()
            self.events.event_attach(vlc.EventType.MediaParsedChanged, self.ParseReceived)
        except Exception as e:
            logging.critical(e)
    
    def ParseReceived(self):
        logging.info('something changed')
        media = self.player.get_media()
        media.parse_with_options(1, 0)
        pass

    def load_station(self,station):
        """ load new station """
        try:
            self.current_station = station
            self.player.set_mrl(station['url'])
        except Exception as e:
            print(e)

    def toggle(self):
        if (self.is_playing):
            logging.warn('stop')
            self.player.stop()
        else:
            logging.warn('start')
            self.player.play()

        self.is_playing = not self.is_playing

    def play(self):
        """play"""
        #Play the media
        try:
            self.player.play()
        except Exception as e:
            logging.warn(e)
        self.is_playing = True

    def get_info(self):
        """ get stream info """
        time.sleep(1)
        info = []

        try:
            media = self.player.get_media()
            media.parse_with_options(1, 0)

            info.append(media.get_meta(0) if media.get_meta(0) else '')
            info.append(media.get_meta(2) if media.get_meta(2) else '')
            info.append(media.get_meta(12) if media.get_meta(12) else '')
        except Exception as e:
            logging.info(e)

        return info 
     

        
