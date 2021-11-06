import unittest
from FileParser import FileParser

class FileParserTest(unittest.TestCase):
    def setUp(self):
        self.fp = FileParser("Test_Input_File.txt")
        pass

    def testCreateList(self):
        urlList = ['https://github.com/cloudinary/cloudinary_npm', 'https://www.npmjs.com/package/express', 'https://github.com/nullivex/nodist', 'https://github.com/lodash/lodash', 'https://www.npmjs.com/package/browserify']
        self.assertTrue(bool(self.fp.URLs))
        self.assertTrue(urlList == self.fp.URLs)

    def testConvertToGithub(self):
        urlList = ['https://github.com/cloudinary/cloudinary_npm', 'https://github.com/expressjs/express', 'https://github.com/nullivex/nodist', 'https://github.com/lodash/lodash', 'https://github.com/browserify/browserify']
        self.assertTrue(bool(self.fp.GitHub_URLS))
        self.assertTrue(urlList == self.fp.GitHub_URLS)

    def testStripUrls(self):
        self.fp.list_of_repos = []
        self.fp.GitHub_URLS = ['https://github.com/cloudinary/cloudinary_npm', 'https://github.com/expressjs/express', 'https://github.com/nullivex/nodist', 'https://github.com/lodash/lodash', 'https://github.com/browserify/browserify']
        urlList = ['https://github.com/cloudinary/cloudinary_npm', 'https://www.npmjs.com/package/express', 'https://github.com/nullivex/nodist', 'https://github.com/lodash/lodash', 'https://www.npmjs.com/package/browserify']
        authorList = ["cloudinary", "expressjs", "nullivex", "lodash", "browserify"]
        nameList = ["cloudinary_npm", "express", "nodist", "lodash", "browserify"]
        self.fp.strip_urls()
        self.assertTrue(bool(self.fp.list_of_repos))
        for x, auth, name, urlTest in zip(self.fp.list_of_repos, authorList, nameList, urlList):
            self.assertTrue(x.author == auth)
            self.assertTrue(x.repo == name)
            self.assertTrue(x.url == urlTest)