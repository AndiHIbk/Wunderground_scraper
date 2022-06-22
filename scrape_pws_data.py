'''
functions used for scraping data from wundermap-pws
pretty quick'n'dirty, but should be working

no error handling or logging, code also needs to be cleaned

latest test on Ubuntu 20.04 with python 3.8


'''

import sys,os,argparse
import datetime, dateutil.rrule
from datetime import timedelta, date, datetime
from selenium import webdriver
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from multiprocessing import Pool
import multiprocessing as mp

#driver = webdriver.Firefox(executable_path='/home/uibk/Downloads/software/geckodriver-v0.31.0-linux64')
#fireFoxOptions = webdriver.FirefoxOptions()
#fireFoxOptions.set_headless()
#driver = webdriver.Firefox(firefox_options=fireFoxOptions)

def getDataLinesFromUrl(url):
    driver = webdriver.Firefox()
    driver.get(url)
    #tab = driver.find_element_by_class_name("history-tabs") # deprecated version
    tab = driver.find_element(By.CLASS_NAME, "history-tabs")
    data = tab.text
    driver.close()
    data_lines = data.split('\n')
    return data_lines
    
def produceURL(statID,date):
    return 'https://www.wunderground.com/dashboard/pws/%s/table/%i-%i-%i/%i-%i-%i/daily'%(statID,
          date.year,date.month,date.day,date.year,date.month,date.day)

def daterange(startDate, endDate):
    for n in range(int((endDate - startDate).days)):
        yield startDate + timedelta(n)
        
def returnListofDates(startDate, endDate):
    listOfDates = []
    for single_date in daterange(startDate, endDate):
        listOfDates.append(single_date)
    return listOfDates

def scrapeToFile(argTup):
	'''
	argtup: ('STATID',date,outfileName)
	'''
	statID,dt = argTup[0],argTup[1]
	URL = produceURL(statID,dt)
	datLines=getDataLinesFromUrl(URL)
	with open (argTup[2],'w') as outfile:
		for l in datLines:
			outfile.write('%s\n'%l.encode('utf-8'))
	# try:
		# statID,dt = argTup[0],argTup[1]
		# URL = produceURL(statID,dt)
		# datLines=getDataLinesFromUrl(URL)
		# with open (argTup[2],'w') as outfile:
			# for l in datLines:
				# outfile.write('%s\n'%l.encode('utf-8'))
	# except:
		# print('failed to scrape %s %s'%(argTup[0],argTup[1]))
    
def main():
	
	#from datetime import date
	
	parser = argparse.ArgumentParser(description="""
	This is a cmd interface for downloading/scraping of wunderground
	PWS Data. please provide the following arguments
	""")
	parser.add_argument('statID', help='Wundermap station id - you get it from the wundermap website', type=str)
	parser.add_argument('datFrom', help='start date pls use <yyyy-mm-dd> format', type=str)
	parser.add_argument('datTo', help='end date pls use <yyyy-mm-dd> format', type=str)
	parser.add_argument('outFolder', help='specify the path/folder to which the data should be written', type=str)

	try:
		args=parser.parse_args()
	except IOError:
		usage()
		sys.exit()
		
	print('\nstarting data download with following options:')
	print('###########################')
	print('Station-ID:\t%s'%args.statID)
	print('date-from:\t%s'%args.datFrom)
	print('date-to:\t%s'%args.datTo)
	print('output Folder:\t%s'%args.outFolder)
	print('###########################\n')
	
	statID = args.statID
	
	startDate = date(int(args.datFrom.split('-')[0]),
	                 int(args.datFrom.split('-')[1]),
	                 int(args.datFrom.split('-')[2]))
	endDate   = date(int(args.datTo.split('-')[0]),
	                 int(args.datTo.split('-')[1]),
	                 int(args.datTo.split('-')[2]))
	
	datDir = args.outFolder
	
	#print(startDate, ' ', endDate)
	#endDate   = 
	# statID='ITIROLAX2'
	# #the date-range, which is downloaded does not include the end-date!!
	# startDate=date(2022,6,14)
	# endDate=date(2022,6,15)
	
	# #datDir='/home/uibkwb/DATA/00_work_data/06_develop/wunderground_scraper/data_raw'
	# datDir='/home/uibk/DATA/02_data/wunderground/test/TEST2022'
	
	# # Make sure a directory exists for the station web pages
	if not os.path.isdir(datDir+'/%s'%statID):
		os.mkdir(datDir+'/%s'%statID)

	loD=returnListofDates(startDate,endDate)
	argList=[(statID,dat,
              datDir+'/%s/%s_%s_%s_%s'%(statID,statID,dat.year,dat.month,dat.day)) for dat in loD]
	
	#p = Pool(8)
	p = Pool(mp.cpu_count()-1)
	p.map(scrapeToFile, argList)
	
	print('finished script')
	sys.exit(0)
		
		
if __name__ == '__main__':
    main()
