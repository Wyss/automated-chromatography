# convert *.ui (Qt file) to *.py (PyQt file)

import glob
import argparse
import subprocess

# cmdline argument handling
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug",
        help="Display pyuic5 debug pyuic5 output.",
        action="store_true")
args = parser.parse_args()

# do the pyuic5 stuff
for file in glob.glob("*.ui"):
    print(file)
    name, _ = file.split(".ui")
    cmd = ["pyuic5", "{}.ui".format(name), "-o", "{}.py".format(name), "-x"]
    if args.debug:
        cmd.append("-d")
    cmd_str = " ".join(cmd)
    print(cmd_str)
    subprocess.call(cmd_str, shell=True)
