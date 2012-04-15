#@PydevCodeAnalysisIgnore
import ctypes
import logging
import win32gui
import win32api

import pwt.config

from win32con import SWP_FRAMECHANGED 
from win32con import SWP_NOMOVE 
from win32con import SWP_NOSIZE 
from win32con import SWP_NOZORDER
from win32con import SW_HIDE
from win32con import SW_FORCEMINIMIZE
from win32con import SW_SHOWNORMAL

from win32con import GW_OWNER 
from win32con import GWL_STYLE 
from win32con import GWL_EXSTYLE 

from win32con import WM_CLOSE 

from win32con import WS_CAPTION 
from win32con import WS_EX_APPWINDOW 
from win32con import WS_EX_CONTROLPARENT
from win32con import WS_EX_TOOLWINDOW

class Window(object):

    def __init__(self, hWindow):

        self.hotkeys = []

        self.hWindow = hWindow
        
        config = pwt.config.config

        self.floating = self.classname in config["window"]["float"].split(";")
        self.decorated = self.classname in config["window"]["decorate"].split(";")

    def __eq__(self, other):

        return self.hWindow == other.hWindow

    def __hash__(self):

        return hash(self.hWindow)

    def validate(self):
        """
        Control some properties of the window to see
        if it should be tiled
        """

        if win32gui.IsWindowVisible(self.hWindow):

            if not win32gui.GetParent(self.hWindow):

                value = win32gui.GetWindowLong(self.hWindow, GWL_EXSTYLE)
                owner = win32gui.GetWindow(self.hWindow, GW_OWNER)

                if (not owner and not value & WS_EX_TOOLWINDOW) or value & WS_EX_APPWINDOW:

                    if not self.floating:

                        return True

        return False

    def is_decorated(self):
        """
        Looks if the window has it's decorations set
        Returns True if it's decorated
        Returns False if it's not decorated
        Returns none on error
        """

        try:

            if win32gui.GetWindowLong(self.hWindow, GWL_STYLE) & WS_CAPTION:

                return True

            else:
            
                return False

        except win32gui.error:

            logging.exception("Error while getting windowstyle")

            return None

    def undecorate(self):
        """
        Removes borders and decoration from window
        Returns True on success
        Returns False on error
        """

        try:

            if not self.decorated:

                style = win32gui.GetWindowLong(self.hWindow, GWL_STYLE)

                style -= WS_CAPTION 

                win32gui.SetWindowLong(self.hWindow, GWL_STYLE, style)

                return True

            return False

        except win32gui.error:

            logging.exception("Error while undecorating the window")

            return False

    def decorate(self):
        """
        Add borders and decoration to window"
        Returns True on success
        Returns False on error
        """

        try:

            style = win32gui.GetWindowLong(self.hWindow, GWL_STYLE)

            style += WS_CAPTION

            win32gui.SetWindowLong(self.hWindow, GWL_STYLE, style)

            return True

        except win32gui.error:

            logging.exception("Error while decorating the window")

            return False

    def toggle_decoration(self):
        """
        Adds or removes decoration
        """

        if self.validate():

            if self.is_decorated():

                self.undecorate()

            else:

                self.decorate()

            self.update()

    def position(self, position):
        """
        Sets the window to the given position
        Returns true on success
        Returns false on error
        """

        try:

            win32gui.MoveWindow(self.hWindow
                    ,position[0]
                    ,position[1]
                    ,position[2] - position[0]
                    ,position[3] - position[1]
                    ,True
            )

            return True

        except win32gui.error:

            logging.exception("Error while placing window")

            return False

    def show(self):
        """
        Puts the window under a shownormal state
        Returns true on succes
        Returns false on error
        """

        try:

            win32gui.ShowWindow(self.hWindow, SW_SHOWNORMAL)

            return True

        except win32gui.error:

            logging.exception("Error while showing window")

            return False

    def hide(self):
        """
        Puts the window under a hidden state
        Returns true on succes
        Returns false on error
        """

        try:

            win32gui.ShowWindow(self.hWindow, SW_HIDE)

            return True

        except win32gui.error:

            logging.exception("Error while hiding window")

            return False

    def is_visible(self):

        try:

            return win32gui.ShowWindow(self.hWindow, SW_SHOWNORMAL)

        except win32gui.error:

            logging.exception("Error while checking visibility")

    def toggle_visibility(self):
        """
        Toggles visibility depending on the current state
        which is fetched from the return of a first ShowWindow
        (doesn't work with getwindowplacement for some reason)
        """

        try:

            if self.is_visible():

                win32gui.ShowWindow(self.hWindow, SW_HIDE)

        except win32gui.error:

            logging.exception("Error while toggling visibility")

    def close(self):
        """
        Sends the close message to the window
        Returns true on succes
        Returns false on error
        """

        try:

            win32gui.SendMessage(self.hWindow, WM_CLOSE, 0, 0)

            return True

        except win32gui.error:

            logging.exception("Error while closing window")

            return False

    def focus(self):
        """
        Puts focus on the window and sets the cursor to the window
        Returns true on succes
        Returns false on error

        """

        try:

            win32gui.SetForegroundWindow(self.hWindow)

            if pwt.config.config.getboolean("global", "center_cursor"):
                self.center_cursor()

            return True

        except win32gui.error:

            logging.exception("Error while focusing window")

            return False

    def update(self):
        """
        Update the window by reposition it on the same place
        Returns True on success
        Returns False on error
        """

        try:

            win32gui.SetWindowPos(self.hWindow
                    ,0
                    ,0
                    ,0
                    ,0
                    ,0
                    ,SWP_FRAMECHANGED + SWP_NOMOVE + SWP_NOSIZE + SWP_NOZORDER
            )

            return True

        except win32gui.error:

            logging.exception("Error while decorating window")

            return False

    def center_cursor(self):
        """
        Moves cursor to the given window
        Returns True on success
        Returns False on error
        """

        try: 

            rect = self.windowrectangle

            win32api.SetCursorPos(((rect[2] + rect[0]) // 2
                ,(rect[3] + rect[1]) // 2))

            return True

        except win32api.error:

            logging.exception("Error while setting the cursor position")

            return False

    def register_shellhook(self):
        """
        Registers a shellhook on the window hWindow
        Returns True on success
        Returns False on error
        """

        if ctypes.windll.user32.RegisterShellHookWindow(self.hWindow):

            return True

        else:

            loggin.warning("Error while registering shellhook")

            return False

    def unregister_shellhook(self):
        """
        Unregisters a shellhook on the window hWindow
        Returns True on success
        Returns False on error
        """

        if ctypes.windll.user32.DeregisterShellHookWindow(self.hWindow):

            return True

        else:

            loggin.warning("Error while unregistering shellhook")

            return False

    def register_hotkeys(self):
        """
        Registers all hotkeys
        Returns True on success
        Returns False on error
        """
        success = True

        for hotkey in self.hotkeys:

            if not hotkey.register(self):

                success = False

        return success

    def unregister_hotkeys(self):
        """
        Unregisters all hotkeys
        """
        success = True

        for hotkey in self.hotkeys:

            hotkey.unregister(self)

    @property
    def windowrectangle(self):
        """
        Returns the window's bounding rectangle
        """

        try: 

            return win32gui.GetWindowRect(self.hWindow)


        except win32gui.error:

            logging.exception("Error while getting the window coordinates")

            return False

    @property
    def classname(self):
        """
        Returns the window's classname
        """

        return win32gui.GetClassName(self.hWindow)


    @property
    def windowmessage(self):
        """
        Returns the message from hWindow's queue
        Returns None on error
        """

        try:

            return win32gui.GetMessage(self.hWindow, 0, 0)

        except win32gui.error:

            logging.exception("Error while grabbing the window message")

            return None

    @staticmethod
    def find_window(classname):
        """
        Finds the window with the given classname
        """

        try:

            return Window(win32gui.FindWindow(classname, None))

        except win32gui.error:

            logging.exception("Error while finding the window")

            return None

      
    @staticmethod
    def focused_window():
        """
        Grabs the current window
        Returns the window on success
        Returns None on error
        """

        try:

            return Window(win32gui.GetForegroundWindow())

        except win32gui.error:

            logging.exception("Error while grabbing the foregroundwindow")

            return None

    @staticmethod
    def window_under_cursor():
        """
        Grabs the window under the cursor
        Returns the window on success
        Returns None on error
        """

        try:

            return Window(win32gui.WindowFromPoint(win32api.GetCursorPos()))

        except win32gui.error:

            logging.exception("Error while grabbing the window from point")

        except win32api.error:

            logging.exception("Error while grabbing the cursor position")

    @staticmethod
    def valid_windows_from_monitor(monitor):
        """
        Enumerates all windows and returns all valid ones
        """

        def callback (hWindow, resultList):
            "Callback function for EnumWindows"

            window = Window(hWindow)

            if window.validate() and monitor.contains_window(window):

                resultList.append(window)

                return True

        windows = []
        win32gui.EnumWindows(callback, windows)

        for window in windows:

            if not window.decorated:
                window.undecorate()

            window.update()

        return windows
