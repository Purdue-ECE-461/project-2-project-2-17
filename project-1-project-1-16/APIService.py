import github
import os
from dotenv import load_dotenv
from URLData import RepoData
import datetime
from git import Repo


class APIService:
    def __init__(self, urls, logger):
        load_dotenv()
        self.logger = logger
        self.token = os.getenv("GITHUB_TOKEN")
        self.github = self.Connect()
        self.urls = urls
        self.urlDataList = []
        self.CreateData()
        self.GetDataFromApi()

    def Connect(self):
        try:
            g = github.Github(self.token)
            self.logger.logToFile("Connection opened to Github", "")
            return g
        except Exception as e:
            self.logger.logToFile("Connection could not be opened to Github", "Check token located in the .env file")
            raise Exception("Failure to connect to Github. Check the Github token.", e.args)

    def CreateData(self):
        for url in self.urls:
            self.urlDataList.append(RepoData(url))
        self.logger.logToFile("RepoData objects created in APIService.py", "")

    def GetDataFromApi(self):
        try:
            for repoData in self.urlDataList:
                repo = self.github.get_repo(repoData.urlObj.author + "/" + repoData.urlObj.repo)
                repoData.stars = repo.stargazers_count
                repoData.openIssues = repo.open_issues_count
                repoData.forks = repo.forks_count
                repoData.repoUsers = repo.subscribers_count
                try:
                    repoData.repoLicense = repo.get_license()
                except:
                    repoData.repoLicense = None
                repoData.repoContributors = repo.get_contributors().totalCount
                split = self.logger.filepath.split("/")
                del split[-1]
                path = ""
                for x in split:
                    path += x + "/"
                if not os.path.exists(path + repoData.urlObj.repo):
                    Repo.clone_from(repoData.urlObj.githubUrl + ".git", path + repoData.urlObj.repo)
                listOfReadMes = ["README.md", "ReadMe.md", "readme.md", "Readme.md", "README.markdown", "ReadMe.markdown", "readme.markdown", "Readme.markdown"]
                for x in listOfReadMes:
                    if (os.path.exists(path + repoData.urlObj.repo + "/" + x) == True):
                        repoData.ReadMe = 1
                        break
                    else:
                        repoData.ReadMe = 0
                monthsSince = -1
                try:
                    for x in repo.get_stats_commit_activity():
                        if x.total > 0:
                            daysSince = datetime.datetime.now() - x.week
                            monthsSince = daysSince.days / 30
                            break
                    if monthsSince == -1:
                        repoData.monthsSinceLastChange = 12
                    else:
                        repoData.monthsSinceLastChange = monthsSince
                except:
                    repoData.monthsSinceLastChange = 12
                    
        except Exception as e:
            self.logger.logToFile("Data could not be obtained from the API", "An error occurred when pulling data. The repo you are testing may not be complete.")
            raise Exception("Data could not be obtained from repo. Check the connection status (Github token) and/or the repo you are trying to pull data from.", e.args)
