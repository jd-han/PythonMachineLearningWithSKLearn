import pandas as pd
import os
import time
from datetime import datetime

#data path where unzipped https://pythonprogramming.net/downloads/intraQuarter.zip
path = "D:/Study/MachineLearning/PythonWithSKLearn/data/intraQuarter"

#'gather' what we try to gater .... target data
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    #as you can see, os.walk will walk around (value) and
    stock_list = [x[0] for x in os.walk(statspath)]
    #print(stock_list)

    # get all files in directory
    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        #print(each_file)
        #time.sleep(15)
        if len(each_file) > 0:
            for file in each_file:

                #file name is the date when it generated ...
                # so take that as date by reg type
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                print(date_stamp, unix_time)
                time.sleep(15)

Key_Stats()