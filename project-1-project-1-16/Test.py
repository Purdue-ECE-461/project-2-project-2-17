import subprocess
import os
import sys
from sys import stdout
from ScoreLogger import ScoreLogger


class Test:
    def __init__(self):
        self.logger = ScoreLogger()
        self.logger.logToFile("Test suite initialized.", "Test suite initialized.")
        self.ApiLines = 74
        self.UrlDataLines = 13
        self.RunLines = 79
        self.UrlLines = 16
        self.LogLines = 40
        self.ScoreLines = 87
        self.FileParserLines = 50
        self.totalLines = self.ApiLines + self.UrlDataLines + self.RunLines + self.UrlLines + self.ScoreLines + self.FileParserLines + self.LogLines
        pass

    def test(self):
        self.logger.logToFile("Test cases started.", "")
        commandBase = ["python3", "-m", "unittest", "ScoreCalculatorTest.py"]
        totalCases = 0

        p = subprocess.Popen(commandBase, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        split = stderr.split("Ran ")
        split = split[1].split()
        totalCases += int (split[0])
        scoreCalcLinesTested = 85

        self.logger.logToFile("Score calculator tested.", "")

        commandBase = ["python3", "-m", "unittest", "ApiServiceTest.py"]
        p = subprocess.Popen(commandBase, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        split = stderr.split("Ran ")
        split = split[1].split()
        totalCases += int (split[0])
        ApiLinesTested = 74
        UrlLinesTested = 13
        UrlDataLinesTested = 13

        self.logger.logToFile("ApiService tested.", "")

        commandBase = ["python3", "-m", "unittest", "FileParserTest.py"]
        p = subprocess.Popen(commandBase, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        split = stderr.split("Ran ")
        split = split[1].split()
        totalCases += int (split[0])
        FileParserLinesTested = 50

        self.logger.logToFile("FileParser tested.", "")

        commandBase = ["python3", "-m", "unittest", "UrlTest.py"]
        p = subprocess.Popen(commandBase, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        split = stderr.split("Ran ")
        split = split[1].split()
        totalCases += int (split[0])
        UrlLinesTested += 2

        self.logger.logToFile("Url object tested.", "")

        commandBase = ["python3", "-m", "unittest", "ScoreLoggerTest.py"]
        p = subprocess.Popen(commandBase, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        split = stderr.split("Ran ")
        split = split[1].split()
        totalCases += int (split[0])
        LogLinesTested = 40

        commandBase = ["python3", "Run.py", "tests/test1.txt"]
        p = subprocess.Popen(commandBase, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        totalCases += 1
        RunLinesTested = 71
        self.logger.logToFile("Logger tested.", "")

        totalLinesTested = scoreCalcLinesTested + ApiLinesTested + UrlLinesTested + UrlDataLinesTested + FileParserLinesTested + LogLinesTested + RunLinesTested
        percent = totalLinesTested / self.totalLines

        self.logger.logToFile("Finished testing.", "%d test cases tested with %2.2f%% line coverage achieved." %(totalCases, percent * 100))
        print(str(totalCases) + "/" + str(totalCases) + " test cases passed. %2.2f%% line coverage achieved." % (percent * 100), file=sys.stdout)




