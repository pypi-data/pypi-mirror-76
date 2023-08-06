import curses
from pymusicterm.ui.widget_set import CustomWidgetSet
import py_cui
import platform
import argparse

import pymusicterm.ui as ui
from pymusicterm.ui.progressbar import LoadingBarWidget
from pymusicterm.ui.windows import LocalPlayerWindow
from pymusicterm.util.system import on_wsl

__version__='0.0.3'

class ImpPyCUI(py_cui.PyCUI):
    
    def __init__(self,num_rows,num_cols) -> None:
        super().__init__(num_rows,num_cols)

    def create_new_widget_set(self, num_rows, num_cols):
        return CustomWidgetSet(num_rows,num_cols,self._logger,simulated_terminal=self._simulated_terminal)

    def _initialize_colors(self):
        super()._initialize_colors()
        curses.init_pair(ui.WHITE_ON_MAGENTA,curses.COLOR_WHITE,curses.COLOR_MAGENTA)

class App:
    """ Main pymusicterm class. Sets the WidgetSet in the beginning
    """

    WINDOWS_OPTIONS=["Local Player","Soon.."]

    def __init__(self,root:ImpPyCUI):
        """ Constructor for App class
        """
        self.root=root

        #Added widgets
        self.status_bar=self.root.status_bar

        self.logo_text_block=self.root.add_block_label(self._get_logo(),0,0,column_span=3)

        #ScrollMenus
        self.menu=self.root.add_scroll_menu("Select a Window",1,1)

        self.__config()

    def _set_widget_set(self):
        option_index=self.menu.get_selected_item_index()
        if option_index==0:
            if on_wsl():
                self.root.show_error_popup("Important","Your system is not supported for this feature")
            else:
                window=LocalPlayerWindow(self.root).create()
                self.root.apply_widget_set(window)
        elif option_index==1:
            self.root.show_message_popup("On development","This function is on development")

    def _set_status_text(self) -> str:
        """ Functions that returns the name of the system the program is runned
        """
        if on_wsl():
            return "WSL"
        else:
            return platform.system()

    def _get_logo(self) -> str:
        """ Generates logo of program

        Returns
        -------
        logo : str
            Returns the logo to be place on a widget
        """
        logo="                                   _        _                   \n"
        logo+=" ___  _ _ ._ _ _  _ _  ___<_> ___ _| |_ ___  _ _ ._ _ _\n" 
        logo+="| . \| | || ' ' || | |<_-<| |/ | ' | | / ._>| '_>| ' ' |\n"
        logo+="|  _/`_. ||_|_|_|`___|/__/|_|\_|_. |_| \___.|_|  |_|_|_|\n"
        logo+="|_|  <___'                                              \n" 

        return logo

    def __config(self):
        """ Function that configure the widgets of the window
        """
        self.menu.add_item_list(self.WINDOWS_OPTIONS)
        self.menu.add_key_command(py_cui.keys.KEY_ENTER,self._set_widget_set)

        self.logo_text_block.set_color(py_cui.MAGENTA_ON_BLACK)

        self.status_bar.set_color(py_cui.BLACK_ON_GREEN)
        self.root.set_title("pymusicterm - {}".format(__version__))
        self.root.toggle_unicode_borders()
        self.root.set_status_bar_text("You're using: {} |q-Quit|Arrow keys to move|Enter - Focus mode".format(self._set_status_text()))

def main():
    """ Entry point for pymusicterm and initialize the CUI
    """
    parser=argparse.ArgumentParser()
    parser.add_argument('--version',action='version',version=__version__)
    args=parser.parse_args()

    root=ImpPyCUI(3,3)
    try:
        wrapper=App(root)
        root.start()
    except py_cui.py_cui.errors.PyCUIOutOfBoundsError:
        print("Your terminal is too small, try increasing it's size")
