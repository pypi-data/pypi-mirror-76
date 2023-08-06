import os
import py_cui
from typing import List

import pymusicterm.ui as ui
from pymusicterm.music import SongFile
from pymusicterm.music.player import MusicPlayer
from pymusicterm.util.file import File,FileMetadata
from pymusicterm.ui.labels import SongInfoBlockLabel
from pymusicterm.ui.widget_set import CustomWidgetSet
from pymusicterm.ui.menus import LocalPlayerQueueMenu, LocalPlayerSettingsMenu, LocalPlayerSongsMenu

class LocalPlayerWindow(MusicPlayer):

    _songs_file:List[SongFile]
    _file_metadata:FileMetadata
    _file:File
    _colums:int = 5
    _rows:int = 7

    window:CustomWidgetSet
    root:py_cui.PyCUI

    def __init__(self,root):
        """ Constructor for LocalPlayerWindow
        """
        #Init of class MusicPlayer, that will initialiaze pygame.mixer
        super().__init__()

        self.root = root
        self.window=self.root.create_new_widget_set(self._rows,self._colums)
        self._file=File()
        self._file_metadata=FileMetadata()

        #Added widgets
        self.status_bar=self.root.status_bar
        self.title_bar=self.root.title_bar

        #BlockLabels
        self.song_info=SongInfoBlockLabel(self.window)

        #Scroll Menus
        self.song_files_menu=LocalPlayerSongsMenu(self.window).create()
        self.settings_menu=LocalPlayerSettingsMenu(self.window).create()
        self.songs_queue_menu=LocalPlayerQueueMenu(self.window).create()
        self.bar=self.progress_bar=self.window.add_progress_bar(6,0,column_span=5)

        self.__load_songs() #TODO: Modify this method to make it async
        self.__config()

    def change_path(self,new_path:str):
        """ Changes file path to search songs
        """
        self._file.set_file_path(new_path)
        self.song_files_menu.clear()
        self.__load_songs()

    def add_song(self):
        """Override of base class function. Adds a new song to the queue
        """
        index=self.song_files_menu.get_selected_item_index()
        song_file=self._songs_file[index]
        # self.song_info.set_song_info(song_file) BUG: In next version py_cui will be fix
        if self.not_in_queue_songs(song_file):
            self._file_metadata.set_file_path(song_file.get_file_path())
            self.songs_queue_menu.add_item(' '.join(self._file_metadata.get_title())) #Adds song to the scroll menu
            super().add_song(song_file) # Method of MusicPLayer class

    def play_song(self, index: int=None) -> str:
        file_path=super().play_song(index)
        self._file_metadata.set_file_path(file_path)
        self.bar.set_total_duration(self._file_metadata.get_length())

    def play(self):
        """Plays a song in queue songs
        """
        index=self.songs_queue_menu.get_selected_item_index()
        self.play_song(index)

    def pause_song(self):
        """ Override of base class function. Pauses the song playing and change
            the color of status bar and title bar
        """
        if self.is_playing():
            super().pause_song() # First it paused
            if self.paused: # Then check if is paused
                self.status_bar.set_color(py_cui.WHITE_ON_RED)
                self.title_bar.set_color(py_cui.WHITE_ON_RED)
            else:
                self.status_bar.set_color(ui.WHITE_ON_MAGENTA)
                self.title_bar.set_color(ui.WHITE_ON_MAGENTA)

    def remove_song(self):
        """ Override of base class function. Removes song from queue
        """
        index=self.songs_queue_menu.get_selected_item_index()
        self.songs_queue_menu.remove_selected_item()
        super().remove_song(index) # Method of MusicPlayer class

    def previous_song(self):
        """ Override of base class function. Plays previous song in queue
        """
        song_index=self.get_song_index()
        if self.is_np_enabled():
            if  song_index > 0:
                super().previous_song() # Method of MusicPlayer class
                song_index=song_index - 1
        self.songs_queue_menu.set_selected_item_index(song_index)

    def next_song(self):
        """ Override of base class function. Plays next song in queue
        """
        song_index=self.get_song_index()
        if self.is_np_enabled():
            if not self.different_path(song_index):
                if song_index < len(self.get_queue_songs())-1:
                    song_index=song_index + 1
                    super().next_song()
            else:
                super().next_song()

        self.songs_queue_menu.set_selected_item_index(song_index)

    def song_time_elapsed(self):
        time_elapsed=super().song_time_elapsed()
        self.bar.increment_items(time_elapsed)

    def change_settings(self):
        index=self.settings_menu.get_selected_item_index()
        if index == 0: # Repeat all
            pass
        elif index == 1: # Repeat Once
            self.set_repeat()
        elif index == 2: # Shuffle
            pass
        elif index == 3:
            self.set_block_np()

    def _show_popup_file_path(self):
        """ Function that show text box popup to get new file path to search file songs
        """
        self.root.show_text_box_popup("Write the path:",self.__validate_path)

    def _show_popup_volume(self):
        self.root.show_text_box_popup("Set Volume from 0 - 100",self.__validate_volume)

    def __validate_path(self,path:str):
        """ Function to validate the path

        Parameters
        ----------
        path : str
            Path to search song files
        """
        if os.path.exists(path):
            self.change_path(path)
        else:
            # Show popup to ask for file path
            self._show_popup_file_path()

    def __validate_volume(self,volume:str):
        if volume.isnumeric() and 0<=int(volume)<=100:
            self.set_volume(int(volume))
        else:
            self._show_popup_volume()

    def __load_songs(self):
        """ Function that loads songs
        """
        songs_name_list:List[str] = []
        self._songs_file=self._file.get_music_list()
        if self._songs_file: #List is not Empty
            songs_name_list=[song.get_name() for song in self._songs_file]
            self.song_files_menu.add_item_list(songs_name_list)
        else:   #List is empty
            self.song_files_menu.clear()

    def __config(self):
        """ Function that configure the widgets of the window (WidgetSet)
        """
        self.status_bar.set_color(ui.WHITE_ON_MAGENTA)

        self.window.add_key_command(py_cui.keys.KEY_S_LOWER,self._show_popup_file_path)
        self.window.add_key_command(py_cui.keys.KEY_SPACE,self.pause_song)
        self.window.add_key_command(py_cui.keys.KEY_P_LOWER,self.previous_song)
        self.window.add_key_command(py_cui.keys.KEY_N_LOWER,self.next_song)
        self.window.add_key_command(py_cui.keys.KEY_V_LOWER,self._show_popup_volume)

        self.settings_menu.add_key_command(py_cui.keys.KEY_ENTER,self.change_settings)
        self.song_files_menu.add_key_command(py_cui.keys.KEY_ENTER,self.add_song)
        self.songs_queue_menu.add_key_command(py_cui.keys.KEY_ENTER,self.play)
        self.songs_queue_menu.add_key_command(py_cui.keys.KEY_BACKSPACE,self.remove_song)

        self.root.set_title("Local Music Player")
        self.root.set_status_bar_text("|q-Quit|S-Search in path|Space-Pause|Arrow keys to move|Enter-Focus Mode")
        self.root.run_on_exit(self.stop_song)
        self.root.title_bar.set_color(ui.WHITE_ON_MAGENTA)

    def create(self) -> py_cui.widget_set.WidgetSet:
        """ Function that returns a window (a widgetset)

        Returns
        -------
        window : WidgetSet
            Returns a widgetset
        """

        return self.window
