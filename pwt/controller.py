#@PydevCodeAnalysisIgnore
from pwt.notifyicon     import NotifyIcon
from pwt.hotkey         import Hotkey
from pwt.monitor        import Monitor
from pwt.window         import Window
from pwt.taskbar        import Taskbar
from pwt.utility        import Utility

import pwt.config

##KEYS
from pwt.hotkey import keys

from win32con import WM_HOTKEY
from win32con import HSHELL_WINDOWCREATED
from win32con import HSHELL_WINDOWDESTROYED
from win32con import CF_TEXT

import win32clipboard

class Controller(object):

    def __init__(self, name):
        """
        Set up the notifyicon and the monitors
        """

        self.group = 0

        self.ICONFOLDER = "icons/"

        #the events that trigger the removal of a window
        self.REMOVE_EVENTS = (HSHELL_WINDOWDESTROYED
                , #placeholder
        )

        #the events that trigger an additional window
        self.ADD_EVENTS = (HSHELL_WINDOWCREATED
                , #placeholder
        )

        self.notifyicon = NotifyIcon(name
                , self.icon
        )

        self.add_hotkeys_to_notifyicon()
        self.notifyicon.register_hotkeys()

        self.notifyicon.register_shellhook() 

        self.taskbar = Taskbar()

        self.monitors = Monitor.display_monitors()

        if self.monitors is not None:

            self.stop = False

        else:

            self.stop = True

    @property
    def icon(self):
        "Return the appropriate icon"

        return self.ICONFOLDER + str(self.group + 1) + ".ico"

    @property
    def current_tiler(self):
        "Returns the current tiler"
        
        return Monitor.current_monitor_from_list(self.monitors).tilers[self.group]

    @property
    def current_group_windows(self):
        "returns all the windows of the current group"

        windows = []

        for monitor in self.monitors:

            windows.extend(monitor.tilers[self.group].windows)

        return windows

    def start(self):
        "start the listeners with a safety try/finally to unregister keys and kill the icon"

        self.notifyicon.show_balloon("Go!", "PWT")

        #Do an initial lookup of all the windows and tile accordingly
        for monitor in self.monitors:

            monitor.tilers[self.group].windows = Window.valid_windows_from_monitor(monitor)
            monitor.tilers[self.group].tile_windows()

        try:

            #message priming read
            message = self.notifyicon.windowmessage

            while message:

                #if message is WM_HOTKEY
                if message[1][1] == WM_HOTKEY:

                    #execute the corresponding hotkeycmd using the id
                    self.notifyicon.hotkeys[message[1][2] - 1].execute()

                #if lparam is an add event
                elif message[1][2] in self.ADD_EVENTS:
                    
                    window = Window(message[1][3])

                    if window not in self.current_group_windows:
                        
                        self.current_tiler.add_window(window)
                    
                #if lparam is a remove event
                elif message[1][2] in self.REMOVE_EVENTS:

                    self.handle_remove_event(Window(message[1][3])
                            , Monitor.monitor_from_point_in_list(self.monitors, message[1][5]))

                if self.stop:

                    self.notifyicon.show_balloon("Stop!", "PWT")
                    break

                #Grab the next message from the message queue
                message = self.notifyicon.windowmessage

        finally:

            #Unregister hotkeys and shellhook
            self.notifyicon.unregister_shellhook()
            self.notifyicon.unregister_hotkeys()

            #Decorate windows
            self.decorate_all_tiledwindows()

            #make sure the taskbar is shown on exit
            self.taskbar.show()

            #Remove icon
            self.notifyicon.destroy()

    def handle_remove_event(self, window, monitor):
        "Triggered when a window needs to be removed"

        tiler = monitor.tilers[self.group]

        tiler.remove_window(window)

    def decorate_all_tiledwindows(self):
        "Decorates all windows in the tiler's memory"

        for monitor in self.monitors:

            for tiler in monitor.tilers:

                for window in tiler.windows:

                    if not window.is_decorated():

                        window.decorate()

                    window.update()
                    window.show()

    def switch_group(self, i):
        "Switch the current group into group i"
        
        for monitor in self.monitors:

            for window in monitor.tilers[self.group].windows:

                window.hide()
            
            for window in monitor.tilers[i].windows:

                window.show()

            monitor.tilers[i].tile_windows()

        self.group = i
        self.notifyicon.draw_icon(self.icon)

        Window.window_under_cursor().focus()

    def send_window_to_tiler(self, window, i):
        "sends window to tiler i"

        currentMonitor = Monitor.monitor_from_window_in_list(self.monitors, window)
        currentTiler = currentMonitor.tilers[self.group] 
        targetTiler = currentMonitor.tilers[i] 

        #hide the window
        if window.validate():

            window.hide()

            #Remove window if it's in the tiler
            if window in currentTiler.windows:

                currentTiler.windows.remove(window)
                currentTiler.tile_windows()

            #Add window if it's not already in the target tiler
            if window not in targetTiler.windows:

                targetTiler.windows.append(window)

    ###
    #Hotkey cmds
    ###

    def cmd_decrease_master_size(self):

        self.current_tiler.decrease_master_size()

    def cmd_increase_master_size(self):

        self.current_tiler.increase_master_size()

    def cmd_focus_next_window(self):

        self.current_tiler.focus_next()

    def cmd_focus_previous_window(self):

        self.current_tiler.focus_previous()

    def cmd_focus_primary_window(self):

        self.current_tiler.focus_primary()

    def cmd_shift_focused_window_down(self):

        self.current_tiler.shift_focused_window_down()

    def cmd_shift_focused_window_up(self):

        self.current_tiler.shift_focused_window_up()

    def cmd_shift_focused_window_to_primary(self):

        self.current_tiler.make_focused_primary()

    def cmd_remove_window_from_master(self):

        self.current_tiler.remove_window_from_master()

    def cmd_add_window_to_master(self):

        self.current_tiler.add_window_to_master()

    def cmd_close_focused_window(self):

        Window.focused_window().close()

    def cmd_switch_to_group_1(self):
        
        if self.group != 0:

            self.switch_group(0)

    def cmd_switch_to_group_2(self):
        
        if self.group != 1:

            self.switch_group(1)

    def cmd_switch_to_group_3(self):
        
        if self.group != 2:

            self.switch_group(2)

    def cmd_switch_to_group_4(self):
        
        if self.group != 3:

            self.switch_group(3)

    def cmd_switch_to_group_5(self):
        
        if self.group != 4:

            self.switch_group(4)

    def cmd_switch_to_group_6(self):
        
        if self.group != 5:

            self.switch_group(5)

    def cmd_switch_to_group_7(self):
        
        if self.group != 6:

            self.switch_group(6)

    def cmd_switch_to_group_8(self):
        
        if self.group != 7:

            self.switch_group(7)

    def cmd_switch_to_group_9(self):
        
        if self.group != 8:

            self.switch_group(8)

    def cmd_send_to_group_1(self):

        if self.group != 0:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 0)

    def cmd_send_to_group_2(self):

        if self.group != 1:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 1)

    def cmd_send_to_group_3(self):

        if self.group != 2:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 2)

    def cmd_send_to_group_4(self):

        if self.group != 3:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 3)

    def cmd_send_to_group_5(self):

        if self.group != 4:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 4)

    def cmd_send_to_group_6(self):

        if self.group != 5:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 5)

    def cmd_send_to_group_7(self):

        if self.group != 6:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 6)

    def cmd_send_to_group_8(self):

        if self.group != 7:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 7)

    def cmd_send_to_group_9(self):

        if self.group != 8:

            window = Window.focused_window() 

            if window:

                self.send_window_to_tiler(window, 8)

    def cmd_focus_next_monitor(self):

        monitor = Monitor.current_monitor_from_list(self.monitors) 

        nextMonitor = Utility.next_item(self.monitors, monitor)

        if nextMonitor and nextMonitor.tilers[self.group].windows:

            window = nextMonitor.tilers[self.group].windows[0]

            if not window.focus():

                nextMonitor.tilers[self.group].remove_window(window)

    def cmd_focus_previous_monitor(self):

        monitor = Monitor.current_monitor_from_list(self.monitors) 

        previousMonitor = Utility.previous_item(self.monitors, monitor)

        if previousMonitor and previousMonitor.tilers[self.group].windows:

            window = previousMonitor.tilers[self.group].windows[0]

            if not window.focus():

                previousMonitor.tilers[self.group].remove_window(window)

    def cmd_shift_to_next_monitor(self):

        window = Window.focused_window()

        if window.validate():

            monitor = Monitor.monitor_from_window_in_list(self.monitors, window) 
            nextMonitor = Utility.next_item(self.monitors, monitor)

            if nextMonitor:
                
                tiler = monitor.tilers[self.group]
                nextTiler = nextMonitor.tilers[self.group]

                if window in tiler.windows:

                    tiler.remove_window(window)

                if window not in nextTiler.windows:

                    nextTiler.add_window(window)

                window.focus()

    def cmd_shift_to_previous_monitor(self):

        window = Window.focused_window()

        if window.validate():

            monitor = Monitor.monitor_from_window_in_list(self.monitors, window) 
            previousMonitor = Utility.previous_item(self.monitors, monitor)

            if previousMonitor:
                
                tiler = monitor.tilers[self.group]
                previousTiler = previousMonitor.tilers[self.group]

                if window in tiler.windows:

                    tiler.remove_window(window)

                if window not in previousTiler.windows:

                    previousTiler.add_window(window)

                window.focus()

    def cmd_choose_next_layout(self):

        self.current_tiler.next_layout()
        self.notifyicon.show_balloon(
                 self.current_tiler.currentLayout.name
                , "LAYOUT"
        )

    def cmd_toggle_focused_window_decoration(self):

        Window.focused_window().toggle_decoration()

    def cmd_stop_pythonwindowstiler(self):
        
        self.stop = True

    def cmd_toggle_taskbar_visibility(self):
        
        self.taskbar.toggle_visibility()

        curmonitor = Monitor.current_monitor_from_list(self.monitors)
        curmonitor.recalc_tiler_dimensions()

        self.current_tiler.tile_windows()

    def cmd_print_focused_window_classname(self):

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(Window.focused_window().classname)
        win32clipboard.CloseClipboard()

        print(Window.focused_window().classname)

    def cmd_tile_focused_window(self):

        self.current_tiler.tile_window(Window.focused_window())

    def cmd_float_focused_window(self):

        self.current_tiler.float_window(Window.focused_window())
        
    def add_hotkeys_to_notifyicon(self):
        
        config = pwt.config.config
        
        for i, func in enumerate(config["hotkey"]):
            
            keycombos = config["hotkey"][func].split("+")
            
            mods = sum([keys[x] for x in keycombos[:-1]])
            
            try: 
                
                vk = keys[keycombos[-1]]
                
            except KeyError:
                
                vk = ord(keycombos[-1].upper())
                
            self.notifyicon.hotkeys.append(Hotkey(
                    i+1
                    , mods
                    , vk
                    , getattr(self, "cmd_" + func)
            ))
        
