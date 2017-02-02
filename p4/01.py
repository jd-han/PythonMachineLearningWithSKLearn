import pandas as pd
import os
import time
from datetime import datetime

#data path where unzipped https://pythonprogramming.net/downloads/intraQuarter.zip #
path = "D:/Study/MachineLearning/PythonWithSKLearn/data/intraQuarter"

#'gather' what we try to gater .... target data#
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    #as you can see, os.walk will walk around (value) and#
    stock_list = [x[0] for x in os.walk(statspath)]
    #print(stock_list)

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        print(each_file)
        time.sleep(15)

Key_Stats()