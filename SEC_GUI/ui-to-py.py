# convert *.ui (Qt file) to *.py (PyQt file)

import glob
# import os
import subprocess
# os.chdir(".")
for file in glob.glob("*.ui"):
    print(file)
    name, _ = file.split(".ui")
    cmd = ["echo", "pyuic5", ".\\{}.ui".format(name), "-o", "{}.py".format(name), "-x"]
    subprocess.call(cmd, shell=True)
    cmd.pop(0)
    subprocess.call(cmd, shell=True)
