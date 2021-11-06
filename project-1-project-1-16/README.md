# project-1-project-1-16
project-1-project-1-16 by Group 16 of ECE 461

To use this program, first run "./run install". This will install dependencies necessary for the program to function.

If "./run [command]" will not run due to permissions, make sure to run "chmod 700 run". This command will update permissions associated with the run file and give it the executable status.

Then run "./run test" to run a test suite on our program.

Finally, run "./run URL_FILE" where "URL_FILE" is the absolute location of a file consisting of an ASCII-encoded newline-delimited set of URLs. These URLs may be in the npmjs.com domain 
(e.g. https://www.npmjs.com/package/even) or come directly from GitHub (e.g. https://github.com/jonschlinkert/even).

Upon successful completion of the program, it will return 0 and the URLs will be printed in descending order of the Net Score for each repository. In the event of an error, the program will return 1 and print out a descriptive message to sys.stderr with a recommendation of next steps.
