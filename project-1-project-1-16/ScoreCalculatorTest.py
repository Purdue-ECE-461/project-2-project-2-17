import unittest
import unittest.mock as mock
from ScoreCalculator import ScoreCalculator


class ScoreCalculatorTest(unittest.TestCase):
    def setUp(self):
        with mock.patch('URLData.RepoData') as MockRepoData:
            self.repoData = MockRepoData
            self.scoreCalc = ScoreCalculator()

    def testRampUpScore(self):
        self.assertTrue(self.scoreCalc.rampUpTimeScore(self.repoData.return_value) == 1)

    def testCorrectnessScore(self):
        returnVals = [(0, 0), (100, .1), (300, .2), (600, .3), (1100, .5), (5000, 1)]
        for x in returnVals:
            self.repoData.stars.return_value = x[0]
            self.assertTrue(self.scoreCalc.correctnessScore(self.repoData.stars.return_value) == x[1])

    def testBusFactorScore(self):
        returnVals = [(500, 0, .75), (1000, 6, .75), (5000, 12, .5)]
        for x in returnVals:
            self.repoData.repoUsers.return_value = x[0]
            self.repoData.monthsSinceLastChange.return_value = x[1]
            self.assertTrue(self.scoreCalc.busFactorScore(self.repoData.repoUsers.return_value,
                                                          self.repoData.monthsSinceLastChange.return_value) == x[2])

    def testResponsivenessScore(self):
        returnVals = [(100, 500, .75), (50, 1000, .75), (5000, 12000, 1), (2, 2, .011)]
        for x in returnVals:
            self.repoData.repoContributors.return_value = x[0]
            self.repoData.forks.return_value = x[1]
            self.assertTrue(self.scoreCalc.responsivenessScore(self.repoData.repoContributors.return_value,
                                                               self.repoData.forks.return_value) == x[2])

    def testLicenseScore(self):
        self.repoData.repoLicense.return_value = None
        self.assertTrue(self.scoreCalc.licenseScore(self.repoData.repoLicense) == 0)

