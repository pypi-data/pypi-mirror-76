# This script is not meant to run, it only provides essential common data
import os

expm = "expm"

# Configurations
## Config files
CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), "CONFIG")
system_wide_config = "/etc/expm/config"
per_user_config = os.path.expanduser("~/.config/expm/config")
current_working_dir_config = os.path.join(os.getcwd(), "expm", ".config")
## Config entries
DEFAULT = "DEFAULT"
### Same as Environment variables
#### EXPMCC
#### EXPMXX

# Environment variables
EXPM_CWD = "EXPM_CWD"
EXPMCC = "EXPMCC"
EXPMXX = "EXPMXX"

# Command line arguments
## Common arguments
arg_expmcc = "--expmcc"
arg_expmxx = "--expmxx"
## Compiler arguments, e.g. gcc/gcc, clang/clang++
args_preprocessing = ["-M", "-MM", "-MF", "-MG", "-MP", "-MT", "-MQ", "-MD", "-MMD"]