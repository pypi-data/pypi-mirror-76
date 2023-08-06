# Pandas Stocks Technical Analysis
---
This is a stocks Trading Project which includes BSE and NSE companies stocks in this we can get data of companies from any past date till current date and it will calculate
technical indicators of desired choice and calculate news sentiment this project also includes a web scraper which extracts news from moneycontrol of required historical years.
---

### Getting Started
---
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Programming Language and Frameowork
---
* Python
* Flask
* Selenium
* pandas
* Numpy
* BeautifulSoup
* Article
* request

### Version Used
---
* Python: 3.7.3

### Library Used
---
**P.S**:*For installation of required library or modules refer [requirement.txt](https://github.com/uday171197/pandas-stocks-tech-analysis/requirements.txt) file and directly install using following command*
		$ pip install -r requirements.txt

### Prerequisites/Requirements
---
* Anaconda
* Atom

### Project Description
---
We used the Bombay stock exchange (BSE) Data to calculate different technical indicators for the batter stock analysis in using pandas.


### Data Source
---
* MySQL database
* NSE API
* www.moneycontrol.com

### Setup Development Environment
---
**Note**:
*Follow below instructions to set up bitbucket account and clone the project structure created on bit bucket to your local machine*
*If you are cloning the complete repository (all programs) or partially created project, then skip below steps and refer **How to directly run partilly created or complete  of other machine or cloned from Bitbucket.***

1. Create a bitbucket repository with suitable project name. *Contact IT Team for the same.*

2. Clone the newly created repo to your workspace. Please create a 'workspace' named directory on the 'D drive' for windows machine and for linux clone in under 'work' directory. *Install git bash for cloning.*

3. How to clone: Open git bash and write the following command.

		$ git clone pathtoyourrepo
		# Enter your bitbucket password if prompted

4. Once cloned, please open the project folder on yourIDE.

5. Open a new terminal on your VS Code IDE. You can click on Terminal widget on navigation bar and new terminal
(shorthand Ctrl+Shift+~).

6. Open explorer and select for a python interpreter (shorthand Ctrl+Shift+P) click on Select Interpreter.

7. Select and activate base conda environment (shorthand Ctrl+Shift+~).

8. Create a new environment for your project using the following command

		$ conda create -n yourprojectenv
		# Type 'y' if conda prompts for installing extra packages.

9. Activate your newly created environment using following command

		$ conda activate yourprojectenv
		# Here yourprojectenv is your environment name.

10. It is recommended to install **pylint** and **formater black** for your IDE. This helps you write your code efficiently.

11. Checkout from **master branch to develop branch.**

12. Add a new **.gitignore** file to ignore unnecessary files which should not be pushed from your local git to server.

13. It is recommended to create and work fetaure branch (master>develop>fetaure).After completing work in fetaure branch, ask seniors to review and approve. Once approved Push it to develop branch. From develop branch after rigorous testing or fixing all bugs it will finally move to master branch which will be our production ready code.

**P.S**:*Always create .yml file at the end of the day. This file helps to clone any other system python-flask environment which includes all required modules to your workspace*
**Use following command to create .yml file.**

		$ conda env export > environment.yml







## Built With

* [Python](https://www.python.org/)


## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.
Please note we have a code of conduct, please follow it in all your interactions with the project.


## Authors

* **Developers**: Uday Gupta, Rahul Dayma



## License

MIT
All rights reserved.
