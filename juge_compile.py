import os
import subprocess

def proccess_directory(directory, pass_condition):
    for file in os.listdir(directory):
        path=os.path.join(directory,file)
        print("Try " + path + " : ", end="")
        process =subprocess.run(['python', 'analyse_syntaxique.py', path, "-v"])
        if process.returncode == 0:
            if pass_condition:
                print("Success")
            else:
                print("Failed")
                exit(1)
        elif process.returncode == 1:
            if not pass_condition:
                print("Success")
            else:
                print("Failed")
                exit(1)
proccess_directory("./input", True)
proccess_directory("./bad_input", False)