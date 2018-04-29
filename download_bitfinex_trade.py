import requests
import pandas as pd
import time

def download_1000(start_TS,symbol):
    url = "https://api.bitfinex.com/v2/trades/t"+symbol+"/hist?start="+str(start_TS)+"&sort=1&limit=1000"
    r = requests.get(url)
    str_list = r.text[2:][:-2].split("],[")
    cols = ['id', 'TS', 'volume', 'price']
    lst = []
    for s in str_list:
        lst.append(s.split(","))
    df = pd.DataFrame(lst, columns=cols)
    return df,str_list[-1].split(",")[1]

def download_from_to(start_TS,end_TS,symbol):
    df_list = []
    start_TS = str(start_TS)
    end_TS = str(end_TS)
    name = "bitfinex_"+symbol+"_"+start_TS+"_"
    i=0
    while(start_TS<end_TS):
        not_ok = True
        while(not_ok):
            try:
                df,T = download_1000(start_TS,symbol)
                print(T)
                not_ok = False
            except Exception as e:
                print(e)
                time.sleep(60)
        start_TS = T
        df_list.append(df)
        i=i+1
        if(i%100==0):
            df = pd.concat(df_list)
            df = df.drop_duplicates()
            df.to_csv(name+".csv",index=False)
    if(len(df_list)>0):
        df = pd.concat(df_list)
        df = df.drop_duplicates()
        df.volume = df.volume.astype(float)
        df.price = df.price.astype(float).fillna(0.0)
        df.to_csv(name+T+".csv",index=False)


t1= 1514764800000
t2= 1522540799000
download_from_to(t1,t2,"BTCUSD")
