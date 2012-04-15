# Python Windows Tiler

PWT is the fruit of my frustration towards the traditional windowing system. There are a few tiling programs for Windows but none of them fit my needs and I wanted to learn win32 programming and Python.

## Install

To run a portable version of PWT download the a directory from build/. 
To launch it with python run pwt.py with a python3.X executable.

## Configure

The default config file currently has 3 sections, global, hotkey and window.

### Global

Center_cursor expects a boolean value to either enable or disable the feature.

  * center_cursor = yes

### Hotkey

The hotkey value expects the form of < modifier+modifier.. >+< key >. [Possible Keys](http://code.google.com/p/python-windows-tiler/source/browse/pwt/hotkey.py)

  * remove_window_from_master = alt+shift+l
  * add_window_to_master = alt+shift+h
  * focus_next_window = alt+j
  * focus_previous_window = alt+k
  * focus_primary_window = alt+return
  * shift_focused_window_down = alt+shift+j
  * shift_focused_window_up = alt+shift+k
  * shift_focused_window_to_primary = alt+shift+return
  * decrease_master_size = alt+h
  * increase_master_size = alt+l
  * close_focused_window = alt+shift+c
  * switch_to_group_1 = alt+1
  * switch_to_group_2 = alt+2
  * switch_to_group_3 = alt+3
  * switch_to_group_4 = alt+4
  * switch_to_group_5 = alt+5
  * switch_to_group_6 = alt+6
  * switch_to_group_7 = alt+7
  * switch_to_group_8 = alt+8
  * switch_to_group_9 = alt+9
  * send_to_group_1 = alt+shift+1
  * send_to_group_2 = alt+shift+2
  * send_to_group_3 = alt+shift+3
  * send_to_group_4 = alt+shift+4
  * send_to_group_5 = alt+shift+5
  * send_to_group_6 = alt+shift+6
  * send_to_group_7 = alt+shift+7
  * send_to_group_8 = alt+shift+8
  * send_to_group_9 = alt+shift+9
  * focus_next_monitor = alt+i
  * focus_previous_monitor = alt+u
  * shift_to_next_monitor = alt+shift+i
  * shift_to_previous_monitor = alt+shift+u
  * choose_next_layout = alt+space
  * toggle_focused_window_decoration = alt+shift+d
  * stop_pythonwindowstiler = alt+shift+delete
  * toggle_taskbar_visibility = alt+v
  * print_focused_window_classname = alt+s
  * tile_focused_window = alt+t
  * float_focused_window = alt+shift+t

### Window 

Window holds the window rules, currently there are 2 rules defined, float and decorate. Due to the nature of some apps they struggle with being tiled. Forcing the decorations on can help get rid of some of the glitches, if that doesn't help you can force float them. If a window gets tiled that shouldn't get tiled you should also add it to float.

The expected format is < window classname >;< window classname >

  * float = `progman;#32770`
  * decorate = `Chrome_WidgetWin_0;ConsoleWindowClass`

### Example 

You can remove keybinds from the config to ignore the entire function as I do in my [My config](http://sourcetumble.appspot.com/my-config-file/).
