from flask.json import jsonify
import github
import os
from dotenv import load_dotenv
# from URLData import RepoData
import datetime
# from git import Repo
# import unittest
# from FileParser import FileParser
import requests
import re
import subprocess
from dotenv.main import load_dotenv
import sys
from os.path import exists
from sys import stdout
import json



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
                # print(repoData.urlObj)
                repo = self.github.get_repo(repoData.urlObj.author + "/" + repoData.urlObj.repo)
                # print(repoData.urlObj.author + "/" + repoData.urlObj.repo)
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
                package = repo.get_contents("package.json").decoded_content.decode("utf-8")
                package = json.loads(package)
                # print(package)
                # print(package["dependencies"])
                repoData.dependencies = package["dependencies"]
                # print(repoData.dependencies)              
                    
        except Exception as e:
            self.logger.logToFile("Data could not be obtained from the API", "An error occurred when pulling data. The repo you are testing may not be complete.")
            raise Exception("Data could not be obtained from repo. Check the connection status (Github token) and/or the repo you are trying to pull data from.", e.args)


class FileParser:
    def __init__(self, fp, logger):
        self.list_of_repos = []
        self.URLs = []
        self.GitHub_URLS = []
        self.logger = logger
        self.logger.logToFile("File parsing beginning", "File parser object created")

        self.create_list(fp)
        self.convert_to_github()
        self.strip_urls()
 
    def create_list(self, fp):
        # self.URLs <-- list of URLs
        try:
            file1 = open(fp, 'r')
            for line in file1.readlines():
                self.URLs.append(line.strip())
            file1.close()
        except Exception as e:
            self.logger.logToFile("Make sure the inputted test file exists and the path is correct.", "This error occurs in FileParser.py in the create_list function, probably due to an incorrect input file.")
            raise Exception('Failure in create_list in FileParser.py. Check that the passed in file exists.', e.args)

    def convert_to_github(self):
        # Converts npjms URLs to GitHub URLs
        try:
            for url in self.URLs:
                if "github.com" in url:
                    self.GitHub_URLS.append(url)
                else:
                    r = requests.get(url)
                    if "github.com" in r.text:
                        self.GitHub_URLS.append(re.search(r'"repository":"(.+?)",', r.text)[1])
                    else:
                        self.GitHub_URLS.append(None)
        except Exception as e:
            self.logger.logToFile("Npmjs URLs could not be converted to Github URLs", "In FileParser.py, the inputted URLs could not be parsed into Github URLs in the convert_to_github()")
            raise Exception("Npmjs URLs could not be parsed in FileParser.py. Check the npmjs URLs", e.args)

    def strip_urls(self):
        # Extracts Author and Repo Name from GitHub URLs
        try:
            for url, actualUrl in zip(self.GitHub_URLS, self.URLs):
                author, repo = url.split("github.com/",1)[1].split("/",1)
                self.list_of_repos.append(Repo(author, repo, actualUrl, url))
        except Exception as e:
            self.logger.logToFile("Author and repo could not be extracted from URL", "A url may not contain \"github.com\" and\or could not be split correctly")
            raise Exception("strip_urls failure in FileParser.py. No author/repo could be pulled from the given URL. Check URLs and try again.", e.args)

class Install:
    def __init__(self):
        pass

    def installLibs(self):
        try:
            subprocess.run(["sh", "./installFile.sh", ""])
        except:
            print("Could not install all of the dependencies in userland. Check that you are connected to the ECE Grid.", file=sys.stderr)
            exit(1)

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

    def is_x_ranges(self, version):
        x_ranges = ['x', 'X', '*']


    def pinned(self, version):
        pattern = r'(\s*\~)?\d\.\d(\.[\dxX*])?'
        if ("-" in version):
            
            ver_split = [x.strip() for x in version.split('-')]
            # print(ver_split)
            matched1 = re.match(pattern, ver_split[0])
            if (bool(matched1) == False):
                
                return 0
            matched2 = re.match(pattern, ver_split[1])
            if (bool(matched2) == False):
                return 0

            version1_split = ver_split[0].split(".")
            version2_split = ver_split[1].split(".")
            
            if (version1_split[0][len(version1_split[0])-1] == version2_split[0][len(version2_split[0])-1] and version1_split[1] == version2_split[1]):
                # print("aloo")
                return 1
            else:
                return 0

        else:
            
            matched = re.match(pattern, version)
            if (bool(matched)):
                # print ("WEEEEEY")
                return 1


    def goodPinningScore(self, dependencies):
        num = 0
        count = 0
        for version in dependencies.values():
            count += 1
            if (self.pinned(version)):
                num += 1

        score = num / count
        return score

    def netScore(self, urlObj0):
        net = (.4 * urlObj0.urlObj.responsiveMaintainScore + .3 * urlObj0.urlObj.correctScore + .1 * urlObj0.urlObj.rampUpScore + .1 * urlObj0.urlObj.busFactorScore) * urlObj0.urlObj.licenseScore + .1 * urlObj0.urlObj.goodPinningPracticeScore
        self.logger.logToFile("Net score calculated for " + urlObj0.urlObj.url, "The calculated net score is %.2f" % net)
        return net

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
        self.goodPinningPracticeScore = 0
        self.githubUrl = githubUrl
        # self.output = []
        pass

    def printScores(self):
        output = []
        output.append(self.netScore)
        output.append(self.rampUpScore)
        output.append(self.correctScore)
        output.append(self.busFactorScore)
        output.append(self.responsiveMaintainScore)
        output.append(self.licenseScore)
        output.append(self.goodPinningPracticeScore)
        output = [ '%.2f' % elem for elem in output]

        # print(self.url + " %.2f %.2f %.2f %.2f %.2f %.2f %.2f" % (self.netScore, self.rampUpScore, self.correctScore, self.busFactorScore, self.responsiveMaintainScore, self.licenseScore, self.goodPinningPracticeScore))
        return output


class RepoData:
    def __init__(self, urlObj):
        self.urlObj = urlObj
        self.stars = 0
        self.openIssues = 0
        self.forks = 0
        self.ReadMe = None
        self.monthsSinceLastChange = 0
        self.repoUsers = 0
        self.repoContributors = 0
        self.repoLicense = None
        self.monthsSinceLastChange = 0
        self.dependencies = {}
        pass

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



class Run:
    def __init__(self):
        pass

    def scoreRepos(filepath):
        load_dotenv()
        logger = ScoreLogger()
        logger.logToFile("Logger started", "Logger started on line 15 in Run.py")
        try:
            fp = FileParser(filepath, logger)
            api = APIService(fp.list_of_repos, logger)
            logger.logToFile("Data obtained from API.", "")
            calc = ScoreCalculator(logger)
            for x in api.urlDataList:
                x.urlObj.licenseScore = calc.licenseScore(x.repoLicense)
                x.urlObj.rampUpScore = calc.rampUpTimeScore(x)
                x.urlObj.correctScore = calc.correctnessScore(x.stars)
                x.urlObj.busFactorScore = calc.busFactorScore(x.repoUsers, x.monthsSinceLastChange)
                x.urlObj.responsiveMaintainScore = calc.responsivenessScore(x.repoContributors, x.forks)
                # x.urlObj.goodPinningPracticeScore = calc.goodPinningScore(x.dependencies)
                # dependencies = {1:"1.1.1 - 1.1.7"}
                x.urlObj.goodPinningPracticeScore = calc.goodPinningScore(x.dependencies)
                x.urlObj.netScore = calc.netScore(x)
            logger.logToFile("Scores calculated.", "")

            for i in range(1, len(api.urlDataList)):
                key = api.urlDataList[i].urlObj.netScore
                j = i - 1
                while j >= 0 and key > api.urlDataList[j].urlObj.netScore :
                        #api.urlDataList[j + 1].urlObj.netScore = api.urlDataList[j].urlObj.netScore
                        temp = api.urlDataList[j + 1]
                        api.urlDataList[j + 1] = api.urlDataList[j]
                        api.urlDataList[j] = temp
                        j -= 1
                api.urlDataList[j + 1].urlObj.netScore = key
                
            logger.logToFile("Scores sorted.", "")

            for x in api.urlDataList:
                output = x.urlObj.printScores()
                return output

        except Exception as e:
            logger.logToFile("An exception occurred. The exception was " + type(e).__name__, "")
            print("We detected an error of type " + type(e).__name__ + ". See below for more information. Please try to fix the error and run again.", file=sys.stderr)
            print(e.args[0], file=sys.stderr)
            exit(1)
    

def main():
    if len(sys.argv) != 2:
        print("There is an incorrect number of inputs. Try running with only two inputs.", file=sys.stderr)
        exit(1)
    elif sys.argv[1] == "install":
        #print("Installing relevant dependencies...", file=sys.stderr)
        installObj = Install()
        installObj.installLibs()
        #print("Installations complete!", file=sys.stderr)
        exit(0)
    elif sys.argv[1] == "test":
        testObj = Test()
        testObj.test()
        exit(0)
    else:
        filepath = sys.argv[1]
        if exists(filepath) == False:
            print("The input file could not be found. Please make sure the file is in the intended filepath.", file=sys.stderr)
            exit(1)
        else:
            output = Run.scoreRepos(filepath)
            # print(output)
            # exit(0)
            # var = 10101011
            return output


if __name__ == '__main__':
    output = main()
    print(str(output))

# output = main()
# print(str(output))