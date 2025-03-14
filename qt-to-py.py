# convert *.ui (Qt file) to *.py (PyQt file)

import sys
# allow imports from parent directory
sys.path.append("..")

import glob
import argparse
import subprocess

# cmdline argument handling
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug",
        help="Display pyuic5 debug pyuic5 output.",
        action="store_true")
args = parser.parse_args()

# gather files
files = glob.glob("**/*.ui", recursive=True)
# files.append(glob.glob("../*.ui"))
print(files)
# do the pyuic5 stuff
for file in files:
    print(file)
    name, _ = file.split(".ui")
    cmd = ["pyuic5", "{}.ui".format(name), "-o", "{}.py".format(name), "-x"]
    if args.debug:
        cmd.append("-d")
    cmd_str = " ".join(cmd)
    print(cmd_str)
    subprocess.call(cmd_str, shell=True)
