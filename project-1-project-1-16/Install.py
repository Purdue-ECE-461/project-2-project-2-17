import subprocess

class Install:
    def __init__(self):
        pass

    def installLibs(self):
        try:
            subprocess.run(["sh", "./installFile.sh", ""])
        except:
            print("Could not install all of the dependencies in userland. Check that you are connected to the ECE Grid.", file=sys.stderr)
            exit(1)