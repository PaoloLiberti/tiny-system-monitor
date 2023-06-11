import subprocess
import re
import threading


# This is platform dependant macOS M1 and provided as an example
# For this module to work powermetrics must be added to sudoers
class GpuUsage(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.usage = 0
        self.pattern = r"GPU \d+ GPU Busy\s+:\s+(\d+\.\d+)%"

    def run(self):
        while True:
            p = subprocess.Popen("sudo powermetrics --samplers gpu_power -i1000 -n1 | grep 'GPU 0 GPU Busy'",
                                 stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p.wait()
            match = re.search(self.pattern, output.decode("utf-8"))
            # print("🚀 ~ file: gpu.py:20 ~ match:", match)
            # print("🚀 ~ file: gpu.py:20 ~ output:", output.decode("utf-8"))
            if match is not None:
                self.usage = float(match.group(1))
