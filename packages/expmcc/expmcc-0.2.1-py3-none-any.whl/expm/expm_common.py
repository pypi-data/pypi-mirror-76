#!/usr/bin/python3
import os
import subprocess
import sys

import expm.common as c

def expm_common(cc_xx): # True:cc False:xx
    # Config
    ## Read from environ
    ## TODO: Read from config files, if not defined in envrion,
    #     when directly executing expmcc/expmxx falls into this situation
    if c.EXPMCC in os.environ:
        compiler_cc = os.environ[c.EXPMCC]
    else:
        compiler_cc = "gcc" # TODO
    if c.EXPMXX in os.environ:
        compiler_cxx = os.environ[c.EXPMXX]
    else:
        compiler_cxx = "g++" # TODO

    # Select compiler
    rest_argv = sys.argv[1:]
    directly_exec = True
    if cc_xx:
        compiler = compiler_cc
        if c.EXPMCC in os.environ:
            directly_exec = False
    else:
        compiler = compiler_cxx
        if c.EXPMXX in os.environ:
            directly_exec = False

    # Execute the original command
    original_command_completed = subprocess.run([compiler] + rest_argv)
    if directly_exec or original_command_completed.returncode!=0:
        sys.exit(original_command_completed.returncode)

    # Get original output absolute path.
    if "-o" not in rest_argv:
        ## Check if is only preprocessing
        is_preprocessing = False
        for arg in c.args_preprocessing:
            if arg in rest_argv:
                is_preprocessing = True
                break
        if is_preprocessing:
            sys.exit()
        ## Find the real path of this source code, be ware of "gcc dir/helloword.c"
        (stdout, stderr) = subprocess.Popen([compiler, "-MM"] + rest_argv, stdout=subprocess.PIPE).communicate()
        if b':' not in stdout:
            sys.exit()
        source_code_path = stdout.split(b':', 1)[1] # b'helloworld.o: dir/helloworld.c\n' => # b' dir/helloworld.c\n'
        if source_code_path.count(b'\n')>1:
            print("Warning!")# TODO: error
            print(["command:"] + [compiler, "-MM"] + rest_argv)
            print(b"stdout" + stdout) 
        source_code_path = source_code_path.replace(b' ', b'').replace(b'\n', b'') # b'dir/helloworld.c'
        rest_argv.append("-o")
        rest_argv.append(source_code_path.decode())
    ## Find "-o"
    output_path_index = rest_argv.index("-o") + 1
    output_path = rest_argv[output_path_index]
    output_path = os.path.abspath(output_path)

    # Modify original output absolute path, 
    # place all expanded-marco source file under directory "expm"
    expm_root_path = os.environ[c.EXPM_CWD]
    common_path = os.path.commonpath([output_path, expm_root_path])
    modified_output_path = os.path.join(
        expm_root_path, c.expm,
        os.path.relpath(output_path, start=common_path))
    ## Create directories if path not exist
    if not os.path.exists(os.path.dirname(modified_output_path)):
        os.makedirs(os.path.dirname(modified_output_path))
    ## Check and Modify the file name
    file_name_suffix_index = modified_output_path.rfind('.')
    if file_name_suffix_index >= 0:
        modified_output_path = modified_output_path[:file_name_suffix_index] # dir/helloworld.ooo => dir/helloworld
    if compiler == compiler_cc:
        modified_output_path += ".c" # dir/helloworld.c
    else:
        modified_output_path += ".cpp" # dir/helloworld.cpp

    rest_argv[output_path_index] = modified_output_path
    subprocess.run([compiler, "-E"] + rest_argv)

def expmcc():
    expm_common(True)

def expmxx():
    expm_common(False)
