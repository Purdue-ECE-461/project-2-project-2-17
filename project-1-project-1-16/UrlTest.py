import unittest
from URL import Repo

class UrlTest(unittest.TestCase):
    def setUp(self):
        self.Repo = Repo("PyGithub", "PyGithub", "https://github.com/PyGithub/PyGithub")
        pass

    def testPrint(self):
        self.assertTrue(self.Repo.printScores())


