import ctypes
import win32gui
import logging

from pwt.window     import Window

from ctypes.wintypes import DWORD
from ctypes.wintypes import HANDLE
from ctypes.wintypes import UINT
from ctypes.wintypes import RECT
from ctypes.wintypes import LPARAM

class APPBARDATA(ctypes.Structure):
            _fields_ = [("cbSize", DWORD),
                    ("hWnd", HANDLE),
                    ("uCallbackMessage", UINT),
                    ("uEdge", UINT),
                    ("rc", RECT),
                    ("lParam", LPARAM)]


class Taskbar(object):

    def __init__(self):

        #taskbar
        self.taskbar = Window.find_window("Shell_TrayWnd")
        self.startbutton = self.get_startbutton()

        self.appbarData = APPBARDATA(ctypes.sizeof(APPBARDATA)
                ,self.taskbar.hWindow
                ,0
                ,0
                ,RECT(0,0,0,0)
                ,0
        )


    def show(self):
        """
        Force show the taskbar
        (and the startbutton)
        """

        self.taskbar.show()
        self.startbutton.show()

        self.autohide_off()

    def toggle_visibility(self):
        """
        Toggle the taskbar's visibility
        (also do the start button to get the desired effect)
        """

        self.taskbar.toggle_visibility()
        self.startbutton.toggle_visibility()

        self.toggle_autohide()

    def get_state(self):
        """
        Fetch the current state of the taskbar
        """

        return ctypes.windll.shell32.SHAppBarMessage(4
                , ctypes.byref(self.appbarData)
        )

    def autohide_on(self):
        """
        Turn autohide on for the taskbar
        """
        self.appbarData.lParam = 1

        ctypes.windll.shell32.SHAppBarMessage(10
                , ctypes.byref(self.appbarData)
        )

    def autohide_off(self):
        """
        Turn autohide off for the taskbar
        """
        self.appbarData.lParam = 0

        ctypes.windll.shell32.SHAppBarMessage(10
                , ctypes.byref(self.appbarData)
        )

    def toggle_autohide(self):
        """
        Toggle the autohide functionality
        """

        if self.get_state() == 1:

            self.autohide_off()

        else:

            self.autohide_on()

    def get_startbutton(self):
        """
        Finds the startbutton
        """

        try:

            desktop = win32gui.GetDesktopWindow()
            return Window(win32gui.FindWindowEx(desktop
                ,None
                ,"button"
                , None
            ))

        except win32gui.error:

            logging.exception("Error while finding the startbutton")

            return None
