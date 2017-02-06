import pandas as pd
import os
import time
from datetime import datetime

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import  style
style.use("dark_background")

import re

#data path where unzipped https://pythonprogramming.net/downloads/intraQuarter.zip
path = "D:/Study/MachineLearning/PythonWithSKLearn/data/intraQuarter"

#'gather' what we try to gater .... target data
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    #as you can see, os.walk will iterate (value) and
    stock_list = [x[0] for x in os.walk(statspath)]
    #print(stock_list)

    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'DE Ratio',
                               'Price',
                               'stock_p_change',
                               'SP500',
                               'sp500_p_change',
                               'Difference'
                               'Status'])

    sp500_df = pd.DataFrame.from_csv("D:/Study/MachineLearning/PythonWithSKLearn/data/YAHOO-INDEX_GSPC.csv")
    #print("YAHOO-INDEX_GSPC.csv", sp500_df)

    ticker_list = []

    # get all files in directory
    #[1:]: will all the file..... for test [1:5]:
    for each_dir in stock_list[1:25]:
        each_file = os.listdir(each_dir)
        #print(each_file)
        #time.sleep(15)

        #want to print ticker(stock value), \\ for \
        ticker = each_dir.split("\\")[1]
        ticker_list.append(ticker)

        #everytime we hit a new ticker we don't need starting point
        starting_stock_value = False
        starting_sp500_value = False

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
                    try:
                        value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                        #print(ticker + ":",value)
                    except Exception as e:
                        value = float(source.split(gather + ':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])
                        #print("line 76 : value"+str(e), ticker, file) #could not convert string to float: 'N/A' , list index out of range
                        print("line 76 : value is : ",value)
                        #time.sleep(15)

                    try:
                        #date what you going to look for
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        '''
                        operations and logic in pandas objects are vectorial. Basically whatever logic/operation you use will be evaluated for all the items stored in the object, and the results will be returned in a new pandas object. For example:
                        pd_object1 = Series([1,1,2,2])
                        pd_object2 = Series([1,1,5,5])
                        print (pd_object1 + pd_object2)
                        ...2
                        ...2
                        ...7
                        ...7
                        print (pd_object1 == pd_object2)
                        ...True
                        ...True
                        ...False
                        ...False

                        In this case I used Series (a Series is like a single column of a dataframe).﻿
                    '''
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                    #259200s = 3days : when it is holiday
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])

                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                        #print("stock_price:", stock_price, "ticker:", ticker)
                    except Exception as e:
                        #<span id="yfs_l10_aig">31.80</span>
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            #print("line 114 : ",stock_price +"\t ticker : "+ticker, "\t file : "+file)
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))

                            print(stock_price)
                            #time.sleep(15)

                        except Exception as e:
                            stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))

                            print('Latest:',stock_price)


                            #print("stock price"+str(e), "\t ticker : "+ticker, "\t file : "+file)
                            #time.sleep(15)
                            #print(str(e), ticker, file)

                    #when starting_stock_value is False we need starting value
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    difference = stock_p_change-sp500_p_change

                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"


                    df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change':stock_p_change,
                                    'SP500':sp500_value,
                                    'sp500_p_change':sp500_p_change,
                                    'Difference':difference,
                                    'Status':status}, ignore_index=True)
                except Exception as e:
                    pass

    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])

            if plot_df['Status'][-1] == "underperform":
                color = 'r'
            else:
                color = 'g'

            plot_df['Difference'].plot(label=each_ticker,color=color)
            plt.legend()
        except:
            pass
    plt.show()

    save = gather.replace(' ','').replace('(','').replace(')','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)


Key_Stats()