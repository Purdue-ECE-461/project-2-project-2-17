class Repo:
    def __init__(self, author, repoName, url, githubUrl):
        self.url = url
        self.author = author
        self.repo = repoName
        self.netScore = 0
        self.rampUpScore = 0
        self.correctScore = 0
        self.busFactorScore = 0
        self.responsiveMaintainScore = 0
        self.licenseScore = 0
        self.githubUrl = githubUrl
        pass

    def printScores(self):
        print(self.url + " %.2f %.2f %.2f %.2f %.2f %.2f" % (self.netScore, self.rampUpScore, self.correctScore, self.busFactorScore, self.responsiveMaintainScore, self.licenseScore))
        return True