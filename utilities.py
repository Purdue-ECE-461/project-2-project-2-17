# Use this file to put any utility functions, such as converting strings
# to zip files or vice-versa, just to help maintain some organization.
import base64
import zipfile
import subprocess

def strToZip(inStr, filename):
    inStrBtes = inStr.encode('utf-8')
    decodeZip = base64.decodebytes(inStrBtes)
    zipFile = open(filename, 'wb')
    zipFile.write(decodeZip)
    zipFile.close()
    return

def auditPackage(filename):
    # Unzip the package
    with zipfile.ZipFile(filename) as package:
        package.extractall()
    # Execute shell commands
    process = subprocess.Popen("cd " + filename[0:-4] + "; npm i --package-lock-only; npm audit", shell=True, stdout=subprocess.PIPE)
    output = process.communicate()
    # print("OUTPUT: ")
    # print(output)
    return output
    
