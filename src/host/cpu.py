# import subprocess
# import re
# import threading

# class CpuTemp(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self, daemon=True)
#         self.temperature = 0
#         self.pattern = r"CPU die temperature: (\d+\.\d+) C"

#     def run(self):
#         print("Running")
#         while True:
#             p = subprocess.Popen("sudo powermetrics --samplers smc | grep 'CPU die temperature'",
#                                  stdout=subprocess.PIPE, shell=True)
#             (output, err) = p.communicate()
#             p.wait()
#             match = re.search(self.pattern, output.decode("utf-8"))
#             print("🚀 ~ file: cpu.py:18 ~ output:", output.decode("utf-8"))
#             print("🚀 ~ file: cpu.py:20 ~ match:", match)
#             if match is not None:
#                 self.temperature = float(match.group(1))

import threading
import subprocess
import re

class CpuTemperature(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.temperature = 0
        self.pattern = r"CPU die temperature: (\d+\.\d+) C"

    def run(self):
        while True:
            p = subprocess.Popen("sudo powermetrics --samplers smc -i1000 -n1 | grep 'CPU die temperature'",
                                 stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p.wait()
            match = re.search(self.pattern, output.decode("utf-8"))
            if match is not None:
                self.temperature = float(match.group(1))
