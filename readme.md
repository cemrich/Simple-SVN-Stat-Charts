# SVN repository statistic charts
This script generates simple statistic charts for small svn repositories.
The charts are embedded in several html files and can be comfortably 
viewed inside your browser.

For plotting the data inside html the javascript [flot library]
(http://www.flotcharts.org/) is used.

## Usage
		python main.py "https://url.to.my/svn/repository"
		
This command will create a directory named "repository" (last part of the 
repository url) inside your current working directory. Open "index.html" 
inside this directory to view the generated statistics.

## Restrictions
This script is in early development and has only been tested on small repositories. 
The script or the chart generation through the may fail when used for bigger 
projects.

In order to get the svn log of the given repository the script calls the systems
"svn" command. This will fail if svn is not installed on your system or the script
is not allowed to execute system calls.