# iAuditor Exporter Tool

## Introduction
The iAuditor Exporter tool is the primary way to bulk export iAuditor information for use in BI tools such as PowerBI. The tool is coded in the Python programming language and can be ran simply and easily on any computer with Python installed.

![Power BI Example](https://safetyculture.github.io/iauditor-exporter/images/powerbi.png)

## [Installation]
The easiest way to run this tool is by installing it as a package. The tool `Pipx` makes this incredibly easy:

* Install Python 3.5+ on the machine you wish to run the tool on
* Create a folder on your machine where you want to store the script. Make sure it's a location you have full access to, your documents folder is usually a good choice. 
* Open a command prompt (If on a Mac, open Terminal. On Windows, use Powershell where possible.)
* Type `cd` and press the space bar once. Drag the folder you just created into the terminal  Window and the path will appear next to your `cd` command
* Press enter
* Run `pip install pipx` (If you get an error, try `pip3 install pipx`)
* Run `pipx install iauditor_exporter`
* Run ia_exporter --setup
* Follow the guidance on screen to configure your config file
* Run ia_exporter --format csv to start your first export. 
* When you next need to run this tool, don't forget to `cd` to the same directory you created above.
* Enjoy!

## [Documentation](https://safetyculture.github.io/iauditor-exporter/)
Extensive documentation is available [here](https://safetyculture.github.io/iauditor-exporter/). Please note this documentation is for a slightly older release of the exporter tool (before it was packaged up.) The installation guide will be updated soon. 