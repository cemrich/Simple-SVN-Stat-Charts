# SVN repository statistic charts
This script generates simple statistic charts for small svn repositories.
The charts are embedded as images in several html files and can be comfortably 
viewed inside your browser.

## Usage
		python main.py "https://url.to.my/svn/repository"
		
This command will create a directory named "repository" (last part of the 
repository url) inside your current working directory. Open "overview.html" 
inside this directory to view the generated statistics.
		
## Generated files
### overview.html (for all users)
- commits by date (stacked bar chart)
- commits by hour (stacked bar chart)
- commits by weekday (pie chart)
- commits by user (pie chart)

### [username].html (one page for every user)
- commits by date (bar chart)
- commits by hour (bar chart)
- commits by weekday (bar chart)

## Restrictions
This script is in early development and has only been tested on small repositories. 
The script or the chart generation through the [google chart api] 
(https://developers.google.com/chart/) may fail when used for bigger projects.

Also note that you need an internet connection to view the generated charts.

In order to get the svn log of the given repository the script calls the systems
"svn" command. This will fail if svn is not installed on your system or the script
is not allowed to execute system calls.