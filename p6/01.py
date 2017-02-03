import pandas as pd
import os
import time
from datetime import datetime

#data path where unzipped https://pythonprogramming.net/downloads/intraQuarter.zip
path = "D:/Study/MachineLearning/PythonWithSKLearn/data/intraQuarter"

#'gather' what we try to gater .... target data
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    #as you can see, os.walk will iterate (value) and
    stock_list = [x[0] for x in os.walk(statspath)]
    #print(stock_list)

    df = pd.DataFrame(columns=['Date','Unix','Ticker','DE Ratio'])

    # get all files in directory
    #[1:]: will all the file..... for test [1:5]:
    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        #print(each_file)
        #time.sleep(15)

        #want to print ticker(stock value), \\ for \
        ticker = each_dir.split("\\")[1]

        if len(each_file) > 0:
            for file in each_file:

                #file name is the date when it generated ...
                # so take that as date by reg type
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp, unix_time)
                #time.sleep(15)

                full_file_path = each_dir + '/' + file
                #print(full_file_path)
                source = open(full_file_path, 'r').read()
                #print(source)
                #time.sleep(15)

                try :
                    value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    #print(ticker + ":",value)
                    df = df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'DE Ratio':value,}, ignore_index=True)
                except Exception as e:
                    pass

    save = gather.replace(' ','').replace('(','').replace(')','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)


Key_Stats()