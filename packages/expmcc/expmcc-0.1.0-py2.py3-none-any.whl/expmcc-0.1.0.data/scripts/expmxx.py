#!python
import sys
import subprocess
import os

import common as c

script_dir = os.path.dirname(os.path.realpath(__file__))
expm_common_path = os.path.join(script_dir, "expm-common.py")
complete = subprocess.run([expm_common_path] + [c.arg_expmxx] + sys.argv[1:])
sys.exit(complete.returncode)