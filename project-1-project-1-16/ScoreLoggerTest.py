import unittest
from ScoreLogger import ScoreLogger

class ScoreLoggerTest(unittest.TestCase):
    def setUp(self):
        self.logger = ScoreLogger()
        self.logger.level = 0
        pass

    def testVerbosity0(self):
        self.logger.logToFile("info", "debug")
        try:
            fptr = open(self.logger.filepath, "r")
            self.assertTrue(1 == 1)
        except(OSError):
            self.assertTrue(1 == 0)

    def testVerbosity1(self):
        self.level = 1
        self.logger.logToFile("info", "debug")
        try:
            fptr = open(self.logger.filepath, "r")
            self.assertTrue(1 == 1)
        except(OSError):
            self.assertTrue(1 == 0)

    def testVerbosity2(self):
        self.level = 2
        self.logger.logToFile("info", "debug")
        try:
            fptr = open(self.logger.filepath, "r")
            self.assertTrue(1 == 1)
        except(OSError):
            self.assertTrue(1 == 0)
            