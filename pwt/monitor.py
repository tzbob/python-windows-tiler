#@PydevCodeAnalysisIgnore
import logging
import win32api

#pwt specific imports
from pwt.tiler import Tiler

from win32con import MONITOR_DEFAULTTONEAREST
from win32con import MONITOR_DEFAULTTOPRIMARY

class Monitor(object):

    def __init__(self, hMonitor):

        self.hMonitor = hMonitor

        self.tilers = []
        
        for i in range(9):

            self.tilers.append(Tiler(self.workarea))
        
    def __eq__(self, other):

        return int(self.hMonitor) == int(other.hMonitor)

    def __hash__(self):

        return hash(self.hMonitor)

    def exists(self):
        """
        Checks if the monitor is still in the current monitor list
        """

        if self in display_monitors():

            return True

        else:

            return False

    def recalc_tiler_dimensions(self):

        for tiler in self.tilers:

            tiler.calc_dimensions(self.workarea)

    def contains_window(self, window):
        """
        Checks if the given window is in the monitor
        Returns true if it is
        Returns false if it is not
        Returns None on error
        """

        try:

            if win32api.MonitorFromWindow(window.hWindow, MONITOR_DEFAULTTONEAREST) == self.hMonitor:

                return True

            else:

                return False

        except win32api.error:

            logging.exception("Error while grabbing monitor from window")
            
            return None

    def is_main(self):
        """
        Looks if the monitor is the main monitor
        """

        try:

            if self.hMonitor == win32api.MonitorFromPoint((0, 0), MONITOR_DEFAULTTOPRIMARY):

                return True

            else:

                return False

        except win32api.error:
        
            logging.exception("Error while grabbing the monitor with point 0,0")

            return None

    def has_point(self, point):
        """
        Looks if the monitor contains the point
        """

        try:

            if self.hMonitor == win32api.MonitorFromPoint(point, MONITOR_DEFAULTTONEAREST):

                return True

            else:

                return False

        except win32api.error:
        
            logging.exception("Error while grabbing the monitor with point")

            return None

    @property
    def workarea(self):
        """
        Returns the work rectangle for the monitor
        Tuple (left, top right, bottom)
        Returns None on error
        """

        try:

            return win32api.GetMonitorInfo(self.hMonitor)["Work"]

        except win32api.error:
            
            logging.exception("Error while getting the monitorinfo")

            return None

    @staticmethod
    def display_monitors():
        """
        Returns all the current monitors
        """

        monitors = []

        try:

            for hMonitor, hdcMonitor, pyRect in win32api.EnumDisplayMonitors():

               monitors.append(Monitor(hMonitor)) 

            return monitors

        except win32api.error:

            logging.exception("Error while enumerating display monitors")

            return None

    @staticmethod
    def main_monitor_from_list(monitors):
        """
        Returns the main monitor
        main monitor is determined by returning the monitor containing
        coordinate 0,0
        """

        for monitor in monitors:

            if monitor.is_main():

                return monitor

    @staticmethod
    def monitor_from_point_in_list(monitors, point):
        """
        Returns the monitor from point
        """

        for monitor in monitors:

            if monitor.has_point(point):

                return monitor

    @staticmethod
    def monitor_from_window_in_list(monitors, window):
        """
        Returns the monitor from the window
        """

        for monitor in monitors:

            if monitor.contains_window(window):

                return monitor

    @staticmethod
    def current_monitor_from_list(monitors):

        return Monitor.monitor_from_point_in_list(monitors,
                win32api.GetCursorPos())
