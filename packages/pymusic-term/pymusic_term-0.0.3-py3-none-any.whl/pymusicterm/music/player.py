import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"
import threading
from pygame import mixer
from typing import List, overload

from pymusicterm.music import SongFile
# https://www.thecodingpup.com/post_detailed/music-player-in-python
class MusicPlayer:
    """ Music player using pygame

    This class uses pygame as a player, which contains functions to control the music. Some 
    of this actions are pause, stop, volume up or down, add or remove song in queue, etc.
    """

    FADE_OUT_TIME:int = 500
    PLAYER_STOPPED:int=0
    NO_QUEUE_SONGS:int=1
    SONG_PLAYING:int=2
    SONG_STOPPED:int=3
    SONG_CHANGING:int=4

    _song_file:SongFile = None
    _queue_songs:List[SongFile] = []
    _main_thread:threading.Thread=None
    _song_index:int = 0
    _status:int=None

    repeat:bool=False
    paused:bool=False
    block_np:bool=False

    def __init__(self):
        """ Constructor for MusicPLayer
        """
        mixer.init() #Initialize pygame

    def set_repeat(self):
        """ Function that sets True/False repeat variable to repeat the song playing
        """
        self.repeat=not self.repeat

    def set_block_np(self):
        """ Function that sets True/False block_np variable to block the keys n and p
        """
        self.block_np=not self.block_np

    def set_volume(self,volume:int):
        """ Sets the volume of the player
        
        Parameters
        ----------
        volume : int
            Value of volume that will be changed (1-100)
        """
        f_volume=volume/100
        mixer.music.set_volume(f_volume)

    def get_song_index(self) -> int:
        """ Gets actual index of the list of queue songs

        Returns
        -------
        song_index : int
            Actual index
        """
        return self._song_index

    def get_queue_songs(self) -> List[str]:
        """ Gets the list of queue songs

        Returns
        -------
        queue_songs : List[str]
            Queue songs
        """
        return self._queue_songs

    def not_in_queue_songs(self,song_file:SongFile) -> bool:
        """Fuction to check if a SongFile that's added already exists in queue songs

        Parameters
        ----------
        song_file : SongFile
            Dataclass where the info of the song file

        Returns
        -------
        exists : bool
            returns if exists
        """
        if not any(song.get_file_path()==song_file.get_file_path() for song in self._queue_songs):
            return True
        return False

    def different_path(self,index:int) -> bool:
        """ Function that checks if the song playing has a different file path

        Returns
        -------
        different : bool
            returns if they are different or not
        """
        if self._song_file.get_file_path() != self._queue_songs[index].get_file_path():
            return True
        return False

    def is_playing(self) -> bool:
        """ Return the current state of the mixer (if is busy)

        Return
        ------
        get_busy : bool
            Check if the music stream is playing
        """
        return mixer.music.get_busy()

    def is_np_enabled(self) -> bool:
        """ Checks if the keys n and p can response when they are pressed
        
        Returns
        -------
        enabled : bool
            Returns if n and p keys are enable when a song is repeating
        """
        if self.block_np and self.repeat:
            return False
        return True

    # -| Function related with the player |-

    def add_song(self,song_file:SongFile):
        """Adds a SongFile to the queue songs

        Parameters
        ----------
        song_file : SongFile
            Dataclass where the info of the song file
        """
        if not self._queue_songs:
            self._status=self.SONG_PLAYING
            self._song_file=song_file # Sets actual SongFile playing
            mixer.music.load(self._song_file.get_file_path()) # Loads the song and play it automatically
            mixer.music.play()
            self._check_player()

        self._queue_songs.append(song_file) # Song added to queue songs

    def remove_song(self, index:int):
        """ Removes song from queue

        Parameters
        ----------
        index : int
            Index of item in queue songs menu
        """
        try:
            del self._queue_songs[index]
        except IndexError:
            pass

    @overload
    def play_song(self) -> str: ... # Function when is replayed the song

    def play_song(self,index:int=None) -> str:
        """ Function that plays a song in queue songs

        Parameters
        ----------
        index : int
            Index of item in queue songs menu

        Returns
        -------
        file_path : str
            File path of the song file
        """
        if self._status==self.NO_QUEUE_SONGS:
            # If every song was played, it will restrart the thread and change status
            self._status=self.SONG_PLAYING
            self._check_player()

        self._status=self.SONG_CHANGING
        if index is not None:
            #! This part is supposed to be executed when player is busy
            # Validate if actual song is playing
            if self.different_path(index):
                self._song_index=index # Sets new index of new song playing
                self._song_file=self._queue_songs[index]
                mixer.music.fadeout(self.FADE_OUT_TIME) # Fadeout until it stops
                mixer.music.load(self._song_file.get_file_path()) # Loads the song and play it automatically
                mixer.music.play()
            else:
                mixer.music.rewind()
        else:
            # Will take the last song selected from the variable _song_file
            mixer.music.load(self._song_file.get_file_path())
            mixer.music.play()
        self._status=self.SONG_PLAYING

        return self._song_file.get_file_path()

    def previous_song(self):
        """ Plays previous song in queue
        """
        self._status=self.SONG_STOPPED
        index = self._song_index - 1
        self.play_song(index)

    def next_song(self):
        """ Plays next song in queue
        """
        self._status=self.SONG_STOPPED
        if self.different_path(self._song_index):
            # Will the play the song in same index if it has a different path
            # (Used when a song is deleted but there are other song in queue ahead)
            index=self._song_index
        else:
            index= self._song_index + 1
        self.play_song(index)

    def pause_song(self):
        """ Pauses the song playing
        """
        if self.paused:
            self.paused=False
            mixer.music.unpause()
        else:
            self.paused=True
            mixer.music.pause()

    def stop_song(self):
        """ Function that stops actual song
        """
        if self._main_thread is not None:
            self._status=self.PLAYER_STOPPED
            self._main_thread.join()
        mixer.music.fadeout(self.FADE_OUT_TIME)

    def song_time_elapsed(self):
        return mixer.music.get_pos()

    def auto_change(self):
        """ Function that automatically changes the song playing or stops the main_thread
        """
        #! This part is supposed to be executed when player is not busy
        max_index=len(self._queue_songs)-1

        #TODO: Handle when queue song list is empty and after the song stopped playing is added a new song
        if not self.repeat:
            # Will check if is the last song and it stills playing
            if self._song_index < max_index and self._status != self.SONG_CHANGING: 
                self.next_song()

            if self._song_index == max_index and self._status==self.SONG_PLAYING:
                # FIXME: When the last song is executed, this part is executed
                self._status=self.NO_QUEUE_SONGS
        else:
            # Will replay the song
            if self._status != self.SONG_CHANGING:
                self.play_song()

    def _check_player(self):
        """ Function that starts a thread to change automatically the song
        """
        def check_player_thread():
            """ Child function that will be runned in a thread
            """
            while self._status!=self.PLAYER_STOPPED and self._status!=self.NO_QUEUE_SONGS:
                if not self.is_playing():
                    self.auto_change()
                else:
                    self.song_time_elapsed()

        self._main_thread=threading.Thread(name="Check Player Thread",target=check_player_thread)
        self._main_thread.start()
