import os.path
import configparser
from collections import OrderedDict

config = configparser.ConfigParser(dict_type=OrderedDict)

if os.path.isfile("config.ini"):

    config.read("config.ini")

else:

    config["global"] = OrderedDict()
    config["global"]["center_cursor"] = "yes"
    config["global"]["left_margin"] = "20"
    config["global"]["right_margin"] = "20"
    config["global"]["top_margin"] = "0"
    config["global"]["bottom_margin"] = "0"
    
    config["hotkey"] = OrderedDict()
    config["hotkey"]["remove_window_from_master"] = "alt+shift+l"
    config["hotkey"]["add_window_to_master"] = "alt+shift+h"
    config["hotkey"]["focus_next_window"] = "alt+j"
    config["hotkey"]["focus_previous_window"] =  "alt+k"
    config["hotkey"]["focus_primary_window"] =  "alt+return"
    config["hotkey"]["shift_focused_window_down"] = "alt+shift+j"
    config["hotkey"]["shift_focused_window_up"] = "alt+shift+k"
    config["hotkey"]["shift_focused_window_to_primary"] = "alt+shift+return"
    config["hotkey"]["decrease_master_size"] = "alt+h"
    config["hotkey"]["increase_master_size"] = "alt+l"
    config["hotkey"]["close_focused_window"] = "alt+shift+c"
    config["hotkey"]["switch_to_group_1"] = "alt+1"
    config["hotkey"]["switch_to_group_2"] = "alt+2"
    config["hotkey"]["switch_to_group_3"] = "alt+3"
    config["hotkey"]["switch_to_group_4"] = "alt+4"
    config["hotkey"]["switch_to_group_5"] = "alt+5"
    config["hotkey"]["switch_to_group_6"] = "alt+6"
    config["hotkey"]["switch_to_group_7"] = "alt+7"
    config["hotkey"]["switch_to_group_8"] = "alt+8"
    config["hotkey"]["switch_to_group_9"] = "alt+9"
    config["hotkey"]["send_to_group_1"] = "alt+shift+1"
    config["hotkey"]["send_to_group_2"] = "alt+shift+2"
    config["hotkey"]["send_to_group_3"] = "alt+shift+3"
    config["hotkey"]["send_to_group_4"] = "alt+shift+4"
    config["hotkey"]["send_to_group_5"] = "alt+shift+5"
    config["hotkey"]["send_to_group_6"] = "alt+shift+6"
    config["hotkey"]["send_to_group_7"] = "alt+shift+7"
    config["hotkey"]["send_to_group_8"] = "alt+shift+8"
    config["hotkey"]["send_to_group_9"] = "alt+shift+9"
    config["hotkey"]["focus_next_monitor"] = "alt+i"
    config["hotkey"]["focus_previous_monitor"] = "alt+u"
    config["hotkey"]["shift_to_next_monitor"] = "alt+shift+i"
    config["hotkey"]["shift_to_previous_monitor"] = "alt+shift+u"
    config["hotkey"]["choose_next_layout"] = "alt+space"
    config["hotkey"]["toggle_focused_window_decoration"] = "alt+shift+d"
    config["hotkey"]["stop_pythonwindowstiler"] = "alt+shift+delete"
    config["hotkey"]["toggle_taskbar_visibility"] = "alt+v"
    config["hotkey"]["print_focused_window_classname"] = "alt+s"
    config["hotkey"]["tile_focused_window"] = "alt+t"
    config["hotkey"]["float_focused_window"] = "alt+shift+t"

    config["window"] = OrderedDict()
    config["window"]["float"] = "progman;#32770"
    config["window"]["decorate"] = "Chrome_WidgetWin_0;ConsoleWindowClass"

    with open("config.ini", "w") as configfile:
        
        config.write(configfile)
