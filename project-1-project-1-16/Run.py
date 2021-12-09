from dotenv.main import load_dotenv
from ScoreCalculator import ScoreCalculator
from APIService import APIService
import sys
from os.path import exists
from FileParser import FileParser
from Test import Test
from ScoreLogger import ScoreLogger
from Install import Install

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
                x.urlObj.printScores()

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
            Run.scoreRepos(filepath)
            exit(0)


if __name__ == '__main__':
    main()