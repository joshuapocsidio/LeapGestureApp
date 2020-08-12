import inspect
import os
import sys
import view.menu.MenuView as ui
import Leap

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../leapLib'))
sys.path.insert(0, lib_dir)

# Initialise Leap motion controller
controller = Leap.Controller()
listener = Leap.Listener()
controller.add_listener(listener)

# Change this kernel type
kernel_type = 'linear'


def main():
    print("Gesture Application Booted")
    ui.show_ui(controller=controller)


if __name__ == '__main__':
    main()
