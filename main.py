import os

import sys
import src.cli as cli
import ctypes

def is_gui_available():
    try:
        # use pyside to check if python's version is supported
        # pyside is not available for py3.14
        import PySide6
    except ImportError:
        return False

    if os.name != 'nt':
        return False

    return True


if __name__ == "__main__":
    if not is_gui_available():
        cli.CLI().run()
    else:
        try:
            from PySide6.QtWidgets import QApplication
            import src.gui as gui

            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                # hide console
                ctypes.windll.user32.ShowWindow(hwnd, 0)

            app = QApplication([])
            g = gui.GUI()
            g.show()
            app.exec()
        except ImportError:
            cli.CLI()
