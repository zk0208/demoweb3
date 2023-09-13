import time

def get_datetime_by_timestamp(timestamp):
    time_array = time.localtime(int(timestamp))
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)

def dataListChangeCandle(dl, exchange, crypto, time_interval) :
    if isinstance(dl, list) != True :
        return None
    else :
        reslists = []
        for row in dl :
            row[0] = get_datetime_by_timestamp(int(row[0])/1000)
            res = [exchange, crypto] + row[0:-1] + [time_interval]
            reslists.append(res)
    return reslists

def dataListChangeRank(dl, exchange, crypto, time_interval) :
    if isinstance(dl, list) != True :
        return None
    else :
        reslists = []
        for row in dl :
            row[0] = get_datetime_by_timestamp(int(row[0])/1000)
            res = [crypto] + [row[0]] + [row[4] * row[5]]
            reslists.append(res)
    return reslists

def dataListChangeCrypto(dl, exchange, cryptolists) :
    if isinstance(dl, dict) != True :
        return None
    else :
        cryinfo = []
        ranking = []
        for crypto in cryptolists :
            res = [exchange.name, crypto]
            if dl[crypto]['timestamp'] is None:
                res.append(get_datetime_by_timestamp(exchange.milliseconds() / 1000))
            else:
                res.append(get_datetime_by_timestamp(dl[crypto]['timestamp'] / 1000))
            res += [dl[crypto]['last'], dl[crypto]['baseVolume']]
            cryinfo.append(res)
            ranking.append(res[1:3]+[res[3] * res[4]])
    return cryinfo, ranking