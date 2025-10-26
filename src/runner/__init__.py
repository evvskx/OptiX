import subprocess
import os, datetime

class Runner:

    def __init__(self):
        self.temp_dir = os.path.join(os.getenv("TEMP"), "OptiX", "Temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.log_file = os.path.join(self.temp_dir, datetime.datetime.now().strftime("Thor_%Y%m%d.txt"))

    def run(self, command):
        proc = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
        )

        out, err = proc.communicate()
        success = proc.returncode == 0

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] Running command: {command}\n")
            f.write(f"[{datetime.datetime.now().isoformat()}] Return Code: {proc.returncode}\n")

        return success
