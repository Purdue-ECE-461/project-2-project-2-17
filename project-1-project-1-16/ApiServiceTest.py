from APIService import APIService
from URL import Repo
import unittest


class TestApiService(unittest.TestCase):

    def setUp(self):
        urls = [Repo("PyGithub", "PyGithub", "https://github.com/PyGithub/PyGithub")]
        self.api = APIService(urls)

    def testConnection(self):
        self.assertTrue(self.api.github is not None)

    def testCreateData(self):
        self.assertTrue(bool(self.api.urlDataList))

    def testStars(self):
        for x in self.api.urlDataList:
            self.assertTrue(x.stars > 0)

    def testForks(self):
        for x in self.api.urlDataList:
            self.assertTrue(x.forks > 0)

    def testOpenIssues(self):
        for x in self.api.urlDataList:
            self.assertTrue(x.openIssues > 0)

    def testRepoLicense(self):
        for x in self.api.urlDataList:
            self.assertTrue(x.repoLicense is not None)

    def testContributors(self):
        for x in self.api.urlDataList:
            self.assertTrue(x.contributors > 0)

    def testReadMe(self):
        for x in self.api.urlDataList:
            self.assertTrue(x.ReadMe is not None)

    def testUsers(self):
        for x in self.api.urlDataList:
            self.assertTrue(x.repoUsers > 0)

    def testMonts(self):
        for x in self.api.urlDataList:
            self.assertTrue(x.monthsSinceLastChange >= 0)
