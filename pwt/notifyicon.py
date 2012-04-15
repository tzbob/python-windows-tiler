#@PydevCodeAnalysisIgnore
import logging
import os

import win32gui
import win32con

from pwt.window import Window

class NotifyIcon(Window):

    def __init__(self, hoverText, icon):

        self.hotkeys = []

        self.hoverText = hoverText
        self.window_class_name = "Notify icon"

        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        classAtom = win32gui.RegisterClass(window_class)

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hWindow = win32gui.CreateWindow(classAtom,
                self.window_class_name,
                style,
                0,
                0,
                win32con.CW_USEDEFAULT,
                win32con.CW_USEDEFAULT,
                0,
                0,
                hinst,
                None)

        win32gui.UpdateWindow(self.hWindow)

        self.notify_id = None
        self.draw_icon(icon)

    def draw_icon(self, icon):

        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)

        if os.path.isfile(icon):

            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            self.hicon = win32gui.LoadImage(hinst,
                    icon,
                    win32con.IMAGE_ICON,
                    0,
                    0,
                    icon_flags)

        else:

            logging.warning("Can't find icon file - using default.")
            self.hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id: 

            message = win32gui.NIM_MODIFY

        else: 
            
            message = win32gui.NIM_ADD

        self.notify_id = (self.hWindow,
                0,
                win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                win32con.WM_USER+20,
                self.hicon,
                self.hoverText)

        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def destroy(self):

        nid = (self.hWindow, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)

    def show_balloon(self, balloontext, balloontitle):
        """
        Shows a balloon notification
        """

        nid = (self.hWindow
                ,0
                ,win32gui.NIF_INFO | win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
                ,win32con.WM_USER+20
                ,self.hicon
                ,self.hoverText
                ,balloontext
                ,1
                ,balloontitle
                ,win32gui.NIIF_INFO) 

        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
