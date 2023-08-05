#!/usr/bin/python3
import os
import subprocess
import sys
import argparse
import configparser

import expm.common as c

def expm():
    #  Config
    ## Read config from config files
    config = configparser.ConfigParser()
    config.read([c.CONFIG, c.system_wide_config, c.per_user_config, c.current_working_dir_config])
    ## Read version number
    script_dir = os.path.dirname(os.path.realpath(__file__))
    VERSION_path = os.path.join(script_dir, "VERSION")
    with open(VERSION_path) as f:
        version_from_file = f.readline()
    ## Config from command line arguments
    parser = argparse.ArgumentParser(
        prog=c.expm,
        description="To generate non-marco version of the source code when compiling.")
    parser.add_argument("--version", "-v", action="version", version=version_from_file)
    parser.add_argument(c.arg_expmcc, metavar="CC", help="set CC as c compiler", dest=c.EXPMCC)
    parser.add_argument(c.arg_expmxx, metavar="CXX", help="set CXX as c++ compiler", dest=c.EXPMXX)
    ### Finish parsing arguments
    (namespace, rest_argv) = parser.parse_known_args()
    ## Combine config from files and config from command line arguments
    for key in vars(namespace):
        if vars(namespace)[key]:
            config[c.DEFAULT][key] = vars(namespace)[key]    
    ## Save this combined config to current working directory
    if not os.path.exists(c.expm):
        os.makedirs(c.expm)
    with open(c.current_working_dir_config, "w+") as cwdcfg:
        config.write(cwdcfg)

    # TODO:Check config
    # e.g. Check whether the compiler exists

    # Set environment variables for child process
    child_env = os.environ.copy()
    child_env[c.EXPM_CWD] = os.path.abspath(os.getcwd())
    child_env[c.EXPMCC] = config[c.DEFAULT][c.EXPMCC]
    child_env[c.EXPMXX] = config[c.DEFAULT][c.EXPMXX]

    # Call child process
    if len(rest_argv)>0:
        subprocess.run(rest_argv, env=child_env)
