#### Short description of wunderground_webscraper and utilities

The code is intended for downloading time-series of meteorological data from Personal Weather Stations (pws), which can be found on http://wunderground.com/wundermap. The user has to provide the ID identifying the station (station-id) and give a date-range for which the data should be downloaded, as well as a directory to which to download the raw-data.
The raw-data consists of single text files, which have to be parsed and merged, to eventually get a single .csv with the whole time-series (currently code for this is not included, but might be at a later stage).

IMPORTANT: 
* The way the web scraping is implemented (remotely open a firefox browser window for every day and then scraping the data tables) is pretty slow - ideally requests for larger time-spans can be run on an otherwise idle machine. 
* Also the availability of data is not checked in advance (should be done manually for the station in question on the wundermap website beforehand).
* Currently no/or just limited logic is implemented for data-checking, handling of missing data, etc.
* Large portions of the code are hardcoded and might not work for e.g. in case of changes to the structure/design of the websites or data-tables
* Meta-Data for the stations is currently not downloaded automatically
	* at least x,y position of the Station in lat,lon is interesting for most applications
	* Metadata can be found on the stations' websites.


##### requirements

The code has been tested with python 3.8.10

###### python packages
The following python packages need to be installed:
* selenium (version 4.2.0)

###### Geckodriver

On Ubuntu 20.04 I downloaded __geckodriver-v0.31.0-linux64.tar.gz__ from https://github.com/mozilla/geckodriver/releases.

The tar.gz. file needs to be unpacked, then made executable with <code>chmod +x geckodriver</code> and eventually copied to /usr/local/bin with <code>sudo mv geckodriver /usr/local/bin/ </code> (alternatively the path with the executable geckodriver can be added to the PATH variable).

##### possible future development
* use a text file with ID, daterange and datdir as input
* write a logfile