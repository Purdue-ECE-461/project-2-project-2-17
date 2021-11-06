class ScoreCalculator:
    def __init__(self, logger):
        self.logger = logger
        self.logger.logToFile("ScoreCalculator created.", "Score calculator created.")
        pass

    def rampUpTimeScore(self, urlObj0):
        if urlObj0.ReadMe == 1:
            self.logger.logToFile("Repo has a ReadMe.", "")
            return 1

        else:
            self.logger.logToFile("Repo does not have a ReadMe", "")
            return 0

    def correctnessScore(self, stars):
        scoreValue = 0
        if stars > 1000:
            scoreValue = .5

        elif stars > 500:
            scoreValue = .3

        elif stars > 250:
            scoreValue = .2

        elif stars > 50:
            scoreValue = .1

        tempStarNum = stars - 1000

        if tempStarNum >= 500:
            scoreValue = scoreValue + ((tempStarNum / 500) / 10)

        if scoreValue > 1:
            scoreValue = 1

        self.logger.logToFile("Repo has a correctness score of %.2f" % scoreValue, "Repo contains %d stars" % stars)
        return scoreValue

    def busFactorScore(self, repoUsers, monthsSinceLastChange):
        scoreVal = .5 * (repoUsers / 1000)
        if scoreVal > .5:
            scoreVal = .5

        scoreVal_changes = .5 * (1 - (monthsSinceLastChange / 12))

        if scoreVal_changes < 0:
            scoreVal_changes = 0

        # if scoreVal_changes > .5:
        #     scoreVal_changes = .5

        scoreVal = scoreVal + scoreVal_changes
        self.logger.logToFile("Repo has a busFactor score of %.2f" % scoreVal, "Repo contains %d users and it has been %d months since the last change to the repo" % (repoUsers, monthsSinceLastChange))
        return scoreVal

    def responsivenessScore(self, contributors, forks):
        scoreVal = contributors / 100
        forkScore = forks / 1000

        if scoreVal > 1:
            scoreVal = 1

        if forkScore > 1:
            forkScore = 1

        scoreVal = .5 * scoreVal + .5 * forkScore
        self.logger.logToFile("Repo has a responsiveness score of %.2f" % scoreVal, "Repo contains %d contributors and %d forks" % (contributors, forks))
        return scoreVal

    def licenseScore(self, repoLicense):
        licenseList = ["MIT", "GPL", "GNU", "Artistic", "boost", "BSD", "bsd", "intel", "ISC", "NCSA", "MPL",
                       "PublicDomain", "Python", "Ruby", "Unicode", "UPL", "Vim", "Wx"]
        if repoLicense is None:
            self.logger.logToFile("Repo does not have a license.", "")
            return 0
        for x in licenseList:
            if (repoLicense.license.spdx_id == x) | (x in repoLicense.license.spdx_id):
                self.logger.logToFile("Repo has a compatible license", "")
                return 1
        self.logger.logToFile("Repo has an incompatible license.", "The license ID is " + repoLicense.license.spdx_id)
        return 0

    def netScore(self, urlObj0):
        net = (.5 * urlObj0.urlObj.responsiveMaintainScore + .3 * urlObj0.urlObj.correctScore + .1 * urlObj0.urlObj.rampUpScore + .1 * urlObj0.urlObj.busFactorScore) * urlObj0.urlObj.licenseScore
        self.logger.logToFile("Net score calculated for " + urlObj0.urlObj.url, "The calculated net score is %.2f" % net)
        return net
