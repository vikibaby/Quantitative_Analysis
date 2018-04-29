import matplotlib.pyplot as plt
import requests
import pandas as pd
import numpy as np
import time
from matplotlib.finance import candlestick_ohlc,candlestick2_ohlc
from datetime import datetime
from matplotlib.dates import DateFormatter,epoch2num
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib

import csv
with open('bitfinex_BTCUSD_1514764800000_1515644112219.csv','rb') as myFile:
        cols = ['StartTime','EndTime','Open','High','Low','Close','Volume','Red','Bid_Ask_Spread','inttime']
        # thetime is depand on the data
        thetime = 1514764800000
        #1Min Bin Data:gap = 60000.
        #5mins bin data: gap = 60000 *5
        gap = 60000
        reader = csv.reader(myFile)


        pricelist = []
        buy_pricelist = []
        sell_pricelist = []
        timelist = []
        volumelist = []
        markvolume=[]
        dfstarttime = []
        dfendtime=[]
        dfopen=[]
        dfhigh=[]
        dflow=[]
        dfclose=[]
        dfvolume = []
        dfred = []
        dfbidask = []
        dfinttime=[]

        for line in reader:

            if line[1] =='TS':
                continue


            if (int(line[1]) > thetime and len(timelist)!= 0):

                pretime = thetime-gap

                starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pretime/1000))
                dfstarttime.append(starttime)

                dfinttime.append(epoch2num(int(pretime/1000)))

                endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(thetime/1000))
                dfendtime.append(endtime)

                dfopen.append(pricelist[0])
                dfhigh.append(max(pricelist))
                dflow.append(min(pricelist))
                dfclose.append(pricelist[-1])
                dfvolume.append(sum(volumelist))

                if sum(markvolume)>0:
                    dfred.append(1)
                else:
                    dfred.append(0)

                if buy_pricelist:
                    buy_price = min(buy_pricelist)
                if sell_pricelist:
                    sell_price = max(sell_pricelist)
                dfbidask.append(buy_price-sell_price)

                timelist = []
                volumelist = []
                markvolume = []
                pricelist = []
                buy_pricelist = []
                sell_pricelist = []
                thetime = thetime+gap

            while (int(line[1]) > thetime and len(timelist) == 0):

                thetime = thetime+gap

            if int(line[1]) <= thetime:

                timelist.append(int(line[1]))
                markvolume.append(float(line[2]))
                volumelist.append(abs(float(line[2])))
                pricelist.append(float(line[3]))
                if float(line[2])>0:
                    buy_pricelist.append(float(line[3]))
                else:
                    sell_pricelist.append(float(line[3]))

        df = pd.DataFrame(columns = cols)
        df["StartTime"]=dfstarttime
        df["EndTime"]=dfendtime
        df["Open"]=dfopen
        df["High"]=dfhigh
        df["Low"]=dflow
        df["Close"]=dfclose
        df["Volume"]=dfvolume
        df["Red"] = dfred
        df["Bid_Ask_Spread"]=dfbidask
        df["inttime"] = dfinttime

        print "done the df"
        df.to_csv('1_min.csv',index=False)
        myfile = df[['inttime','Open','High','Low','Close','Volume']]

        fig = plt.figure()
        fig.subplots_adjust(bottom=0.4)
        f1 = plt.subplot2grid((6,4), (1,0), rowspan=6, colspan=4, axisbg='#07000d')

        xfmt = DateFormatter('%Y-%m-%d %H:%M:%S')
        f1.xaxis.set_major_formatter(xfmt)
        candlestick_ohlc(f1, myfile.as_matrix(), width=0.0001, colorup='#77d879', colordown='#db3f3f', alpha=1)
        f1.xaxis_date()
        f1.autoscale_view()

        plt.xticks(rotation=90)
        plt.xlabel('time')
        plt.ylabel('Price')
        plt.title('1_min_Bid_Ask_Spread')
        f1.grid(True)
        plt.savefig('1_min_Bid_Ask_Spread.png')
        plt.show()
        plt.close()
