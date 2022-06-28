'''
functions used for parsing data from wundermap-pws
which has been downloaded with scrape_pws_data.py

code handles conversions from Imperial to Metric units if necessary

however still hardcoded a lot!
no error handling or logging, code also needs to be cleaned

latest test on Ubuntu 20.04 with python 3.8

'''

import sys,os
import datetime, dateutil.rrule
from datetime import timedelta, date, datetime
import argparse

def merge_csv(inDir,outfile):
    '''
    merges all .csv files in a folder into one csv
    in a defined location
    '''
    with open(outfile,'w') as fout:
        for i,fname in enumerate(os.listdir(inDir)):
            if i == 0:
                fin_lines = open(inDir+'/'+fname,'r').readlines()
            else:
                fin_lines = open(inDir+'/'+fname,'r').readlines()[1:]

            for l in fin_lines:
                fout.write(l)

def raw_to_csv(fnIn,fnOut):
    '''
    parse "raw-data" for daily files downloaded with scrape_pws_data.py
    and convert data formats if necessary
    then write a .csv file which can be processed further
    '''  
    with open(fnIn,'rb') as infile:
        #print(infile.readlines())
        outfile=open(fnOut,'w')
        outfile.write('datetime;temp;dewPoint;humidity;wDir;wAvg;wGust;pressure;pI;pCum\n')
        
        for i,lineOrig in enumerate(infile.readlines()):
            #skipping rows 1,2
            line = lineOrig.decode('UTF-8')[2:-2]
            #print(lineOrig)
            #line = lineOrig
            if i == 2:
                dt=datetime.strptime(line,'%B %d, %Y').date()
                pass
            if i>3:
                lParsed=parseLine(line,dt)
                outfile.write('%s;%.2f;%.2f;%.2f;%s;%.2f;%.2f;%.2f;%.2f;%.2f\n'%lParsed)

def parseLine(line,dt):
    '''
    parse a single line and convert imperial units to metric units if
    imperial units are detected in the line.
    If the parsing does not work, then noData values are assigned to
    the line ('Nan' in case of strings, -9999 in case of numeric data)
    '''
    try:
        time24 = datetime.strptime((" ".join(line.split()[:2])), '%I:%M %p').time()
        ts = "%s %s"%(dt,time24)
        #print(ts)
        if line.split()[3][-1] == 'F':
            temp = round((float(line.split()[2][:-1]) -32.) * (5/9.),2)
        else:
            temp = round((float(line.split()[2][:-1])),2)
        if line.split()[3][-1] == 'F':
            dewP = round((float(line.split()[4][:-1]) -32.) * (5/9.),2)
        else:
            dewP = round((float(line.split()[4][:-1])),2)    
            
        hum = float(line.split()[6][:-1])*0.01
        wD = line.split()[8]
        
        if line.split()[10][-3:] == 'mph':
            wS = round(float(line.split()[9])*1.60934,2)
            wG = round(float(line.split()[11])*1.60934,2)
        else:
            wS = round(float(line.split()[9]),2)
            wG = round(float(line.split()[11]),2)
        
        if line.split()[14][-2:] == 'in':
            p = round(float(line.split()[13])*25.4,2)
            pI = round(float(line.split()[15])*25.4,2)
            pC = round(float(line.split()[17])*25.4,2)
        else:
            p = round(float(line.split()[13]),2)
            pI = round(float(line.split()[15]),2)
            pC = round(float(line.split()[17]),2)
    except:
        ts,temp,dewP,hum='NaN',-9999,-9999,-9999
        wD,wS,wG,p,pI,pC='NaN',-9999,-9999,-9999,-9999,-9999
        
    return(ts,temp,dewP,hum,wD,wS,wG,p,pI,pC)
        

def main():
    
    parser = argparse.ArgumentParser(description="""
    This is a cmd interface for parsing of the downloaded
    pws data and writing .csv files from them.
    """)
    parser.add_argument('inDir', help='directory where the raw-data from scrape_pws_data has been stored (NO "/" AT THE END OF THE PATH)', type=str)
    parser.add_argument('outDir', help='output directory for parsed and converted .csv files (one file per day) (NO "/" AT THE END OF THE PATH)', type=str)

    try:
        args=parser.parse_args()
    except IOError:
        usage()
        sys.exit()
    
    outDir = args.outDir
    inDir  = args.inDir
    
    print(inDir)
    print(outDir)
    
    if not os.path.isdir(outDir):
        print('creating output directory %s'%(outDir))
        os.mkdir(outDir)
    
    for fname in os.listdir(inDir):
        if os.path.isfile(inDir+'/'+fname):
            raw_to_csv(inDir+'/'+fname,outDir+'/'+fname+'_mod.csv')
            print('finished processing %s'%fname)


if __name__ == '__main__':
    main()
