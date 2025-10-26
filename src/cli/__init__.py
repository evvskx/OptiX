import os
import re
import sys
import msvcrt
import threading
import time
from colorama import init, Fore, Back, Style
from jobs import jobs
from runner import Runner
import ctypes

class CLI:
    def __init__(self):
        init(autoreset=True)
        self.running = True
        self.options = ["Optimize", "Exit"]
        self.selected = 0
        self.ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        self.menu_lines_count = 11 
        self.hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        self.force_fullscreen()

    def force_fullscreen(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 3)
        ctypes.windll.user32.SetForegroundWindow(self.hwnd)

    def clear_menu_area(self):
        for _ in range(self.menu_lines_count):
            print('\x1b[1A\x1b[2K', end='')

    def get_terminal_size(self):
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines
        except OSError:
            return 80, 24

    def center_text(self, text, width):
        clean_text = self.ansi_escape.sub('', text)
        length = len(clean_text)
        if length >= width:
            return text
        spaces_left = (width - length) // 2
        spaces_right = width - length - spaces_left
        return ' ' * spaces_left + text + ' ' * spaces_right

    def draw_menu(self):
        self.force_fullscreen()
        os.system("cls")
        width, height = self.get_terminal_size()
        box_width = min(60, width - 4)
        lines = []
        lines.append("=" * box_width)
        lines.append("|" + " " * (box_width - 2) + "|")
        title = Fore.YELLOW + Style.BRIGHT + "OptiX" + Style.RESET_ALL
        lines.append("|" + self.center_text(title, box_width - 2) + "|")
        desc = "An advanced, fast, one-click Windows optimizer"
        lines.append("|" + self.center_text(desc, box_width - 2) + "|")
        lines.append("|" + " " * (box_width - 2) + "|")
        for i, option in enumerate(self.options):
            button_text = f"[ {option} ]"
            if i == self.selected:
                button_text = Fore.BLACK + Back.GREEN + Style.BRIGHT + button_text + Style.RESET_ALL
            lines.append("|" + self.center_text(button_text, box_width - 2) + "|")
        lines.append("|" + " " * (box_width - 2) + "|")
        lines.append("=" * box_width)

        total_lines = len(lines)
        pad_top = max((height - total_lines) // 2, 0)
        print("\n" * pad_top, end='')
        pad_left = max((width - box_width) // 2, 0)
        for line in lines:
            print(" " * pad_left + line)

    def run(self):
        while self.running:
            self.draw_menu()
            key = self.get_key()
            if key == 'UP':
                self.selected = (self.selected - 1) % len(self.options)
            elif key == 'DOWN':
                self.selected = (self.selected + 1) % len(self.options)
            elif key == 'ENTER':
                self.handle_selection()
            self.clear_menu_area()

    def get_key(self):
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':
                    key2 = msvcrt.getch()
                    if key2 == b'H':
                        return 'UP'
                    elif key2 == b'P':
                        return 'DOWN'
                elif key == b'\r':
                    return 'ENTER'

    def handle_selection(self):
        choice = self.options[self.selected]
        if choice == "Optimize":
            self.__optimize()
        elif choice == "Exit":
            self.running = False

    def __optimize(self):
        spinner_frames = [
            f"{Fore.RED}[ {Fore.WHITE}*{Fore.LIGHTBLACK_EX}* {Fore.RED}]",
            f"{Fore.RED}[ {Fore.LIGHTBLACK_EX}*{Fore.WHITE}* {Fore.RED}]"
        ]
        stop_spinner = False

        def spinner(action):
            i = 0
            while not stop_spinner:
                frame = spinner_frames[i % len(spinner_frames)]
                sys.stdout.write(Fore.YELLOW + f"{frame}" + Fore.WHITE + f" :: {action}\r")
                sys.stdout.flush()
                time.sleep(0.25)
                i += 1

        os.system("cls")
        print(Fore.CYAN + Style.BRIGHT + "[ =========================== OptiX =========================== ]\n" + Style.RESET_ALL)

        for job in jobs:
            for category, tasks in job.items():
                print(Fore.YELLOW + f":: {category}" + Style.RESET_ALL)
                for action, command in tasks.items():
                    stop_spinner = False
                    spinner_thread = threading.Thread(target=spinner, args=(action,), daemon=True)
                    spinner_thread.start()
                    current_job = Runner().run(command)
                    stop_spinner = True
                    spinner_thread.join()

                    sys.stdout.write("\r" + " " * 80 + "\r")
                    if current_job:
                        sys.stdout.write(Fore.WHITE + f"[ {Fore.GREEN}OK {Fore.WHITE}] :: {action}\n")
                    else:
                        sys.stdout.write(Fore.WHITE + f"[ {Fore.RED}NO {Fore.WHITE}] :: {action}\n")
                    sys.stdout.flush()

        print(Fore.GREEN + Style.BRIGHT + "\nOptiX has optimized your PC successfully!" + Style.RESET_ALL)
        os.system('shutdown -r -f -t 15 -c "Your PC is going to restart to apply Thor\'s optimizations."')

if __name__ == "__main__":
    cli = CLI()
    cli.run()
