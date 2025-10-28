import os
import sys
import src.cli as cli

def is_gui_available():
    try:
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

            app = QApplication([])
            g = gui.GUI()
            g.show()
            app.exec()
        except ImportError:
            print("PySide6 is not installed. Falling back to CLI mode.")
            cli.CLI()
