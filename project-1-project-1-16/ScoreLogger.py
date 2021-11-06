from dotenv import load_dotenv
import os
import datetime

class ScoreLogger:
    def __init__(self):
        load_dotenv()
        self.filepath = os.getenv("LOG_FILE")
        self.level = int(os.getenv("LOG_LEVEL"))

        if (os.path.exists(self.filepath) != True):
            split = self.filepath.split("/")
            del split[-1]
            path = ""
            for x in split:
                path += x + "/"
            os.makedirs(path, exist_ok=True)
            fptr = open(self.filepath, "x")
            fptr.close()

        fptr = open(self.filepath, "a")
        fptr.write("\n\n")
        fptr.close()
        pass

    def logToFile(self, infoMessage, debugMessage):
        if (os.path.exists(self.filepath) != True):
            fptr = open(self.filepath, "x")
            fptr.close()

        if (self.level >= 1):
            fptr = open(self.filepath, "a")
            fptr.write("Informational Message: " + infoMessage + "\n")
            fptr.close()
            
        if (self.level == 2):
            fptr = open(self.filepath, "a")
            fptr.write("DEBUG Message: " + debugMessage + "\n")
            fptr.close()
        
        return self.level
