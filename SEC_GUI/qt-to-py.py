# convert *.ui (Qt file) to *.py (PyQt file)

import glob
# import os
import subprocess
# os.chdir(".")
for file in glob.glob("*.ui"):
    print(file)
    name, _ = file.split(".ui")
    cmd = ["pyuic5", "{}.ui".format(name), "-o", "{}.py".format(name), "-x"]
    cmd_str = " ".join(cmd)
    print(cmd_str)
    subprocess.call(cmd_str, shell=True)
