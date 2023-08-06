import requests

class ExchangeEndpoints(object):
    def __init__(self, key = "api-key-not-specified", secret = "api-secret-not-specified"):
        self.key = key
        self.secret = secret
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.key,
            'X-API-SECRET': self.secret
        }

    """
    Lists all exchanges that we support.
    Reference: https://docs.blockfacts.io/?python#all-exchanges
    """
    def listAllExchanges(self):
        response = requests.get('https://api.blockfacts.io/api/v1/exchanges', headers=self.headers)
        return response.json()
  
    """
    Gets information about a specific exchange by its name. Returns information such as which assets are supported, asset ticker info, etc.
    @param {string} exchange 
    Reference: https://docs.blockfacts.io/?python#specific-exchange-data
    """
    def getSpecificExchangeData(self, exchange):
        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/' + str(exchange), headers=self.headers)
        return response.json()

    """
    Gets the Blockfacts pair representation of the provided exchange pair
    @param {string} exchange
    @param {string} pair  
    Reference: https://docs.blockfacts.io/?python#pair-info
    """
    def getPairInfo(self, exchange, pair):
        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/pair-info?exchange=' + str(exchange) + "&pair=" + str(pair), headers=self.headers)
        return response.json()   
  
    """
    Gets current trade data for specific asset-denominator pair, from specific exchange(s).
    @param {list/string} assets Asset list or comma-separated string.
    @param {list/string} denominators Denominator list or comma-separated string.
    @param {list/string} exchanges Exchange list or comma-separated string.
    Reference: https://docs.blockfacts.io/?python#current-trade-data
    """
    def getCurrentTradeData(self, assets, denominators, exchanges):
        assetsString = ""
        denominatorsString = ""
        exchangesString = ""

        if type(assets) != list and type(assets) != str:
            raise Exception("Parameter 'assets' must be of 'str' or 'list' type")

        if type(denominators) != list and type(denominators) != str:
            raise Exception("Parameter 'denominators' must be of 'str' or 'list' type")

        if type(exchanges) != list and type(exchanges) != str:
            raise Exception("Parameter 'exchanges' must be of 'str' or 'list' type")

        if isinstance(assets, list):
            assetsString = ','.join([str(x) for x in assets])
        else:
            assetsString = assets

        if isinstance(denominators, list):
            denominatorsString = ','.join([str(x) for x in denominators])
        else:
            denominatorsString = denominators

        if isinstance(exchanges, list):
            exchangesString = ','.join([str(x) for x in exchanges])
        else:
            exchangesString = exchanges

        assetsString = assetsString.replace(" ", "")
        denominatorsString = denominatorsString.replace(" ", "")
        exchangesString = exchangesString.replace(" ", "")

        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/trades?asset=' + assetsString + "&denominator=" + denominatorsString + "&exchange=" + exchangesString, headers=self.headers)
        return response.json()  

    """
    Gets 600 latest trades that happened on the requested exchange(s) and pairs.
    @param {list/string} assets Asset list or comma-separated string.
    @param {list/string} denominators Denominator list or comma-separated string.
    @param {list/string} exchanges Exchange list or comma-separated string.
    Reference: https://docs.blockfacts.io/?python#snapshot-trade-data
    """
    def getSnapshotTradeData(self, assets, denominators, exchanges):
        assetsString = ""
        denominatorsString = ""
        exchangesString = ""

        if type(assets) != list and type(assets) != str:
            raise Exception("Parameter 'assets' must be of 'str' or 'list' type")

        if type(denominators) != list and type(denominators) != str:
            raise Exception("Parameter 'denominators' must be of 'str' or 'list' type")

        if type(exchanges) != list and type(exchanges) != str:
            raise Exception("Parameter 'exchanges' must be of 'str' or 'list' type")

        if isinstance(assets, list):
            assetsString = ','.join([str(x) for x in assets])
        else:
            assetsString = assets

        if isinstance(denominators, list):
            denominatorsString = ','.join([str(x) for x in denominators])
        else:
            denominatorsString = denominators

        if isinstance(exchanges, list):
            exchangesString = ','.join([str(x) for x in exchanges])
        else:
            exchangesString = exchanges

        assetsString = assetsString.replace(" ", "")
        denominatorsString = denominatorsString.replace(" ", "")
        exchangesString = exchangesString.replace(" ", "")

        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/trades/snapshot?asset=' + assetsString + "&denominator=" + denominatorsString + "&exchange=" + exchangesString, headers=self.headers)
        return response.json()

    """
    Gets the snapshot of provided exchange(s) OHLCV data for provided asset-denominator pairs and intervals.
    @param {list/string} assets Asset list or comma-separated string.
    @param {list/string} denominators Denominator list or comma-separated string.
    @param {list/string} exchanges Exchange list or comma-separated string.
    @param {list/string} intervals Interval list or comma-separated string.
    Reference: https://docs.blockfacts.io/?python#data-snapshot-ohlcv-exchange
    """
    def getOHLCVSnapshotData(self, assets, denominators, exchanges, intervals):
        assetsString = ""
        denominatorsString = ""
        intervalsString = ""
        exchangesString = ""

        if type(assets) != list and type(assets) != str:
            raise Exception("Parameter 'assets' must be of 'str' or 'list' type")

        if type(denominators) != list and type(denominators) != str:
            raise Exception("Parameter 'denominators' must be of 'str' or 'list' type")

        if type(intervals) != list and type(intervals) != str:
            raise Exception("Parameter 'intervals' must be of 'str' or 'list' type")

        if type(exchanges) != list and type(exchanges) != str:
            raise Exception("Parameter 'exchanges' must be of 'str' or 'list' type")

        if isinstance(assets, list):
            assetsString = ','.join([str(x) for x in assets])
        else:
            assetsString = assets

        if isinstance(denominators, list):
            denominatorsString = ','.join([str(x) for x in denominators])
        else:
            denominatorsString = denominators

        if isinstance(intervals, list):
            intervalsString = ','.join([str(x) for x in intervals])
        else:
            intervalsString = intervals

        if isinstance(exchanges, list):
            exchangesString = ','.join([str(x) for x in exchanges])
        else:
            exchangesString = exchanges

        assetsString = assetsString.replace(" ", "")
        denominatorsString = denominatorsString.replace(" ", "")
        intervalsString = intervalsString.replace(" ", "")
        exchangesString = exchangesString.replace(" ", "")

        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/trades/ohlcv-snapshot?asset=' + assetsString + "&denominator=" + denominatorsString + "&exchange=" + exchangesString + "&interval=" + intervalsString, headers=self.headers)
        return response.json()

    """
    Gets exchange historical price by asset-denominator, exchange, date, time and interval.
    @param {string} asset 
    @param {string} denominator 
    @param {list/string} exchanges 
    @param {string} date 
    @param {string} time 
    @param {int} interval 
    @param {int} page 
    Reference: https://docs.blockfacts.io/?python#historical-trade-data
    """
    def getHistoricalTradeData(self, asset, denominator, exchanges, date, time, interval, page=None):        
        exchangesString = ""

        if type(exchanges) != list and type(exchanges) != str:
            raise Exception("Parameter 'exchanges' must be of 'str' or 'list' type")

        if isinstance(exchanges, list):
            exchangesString = ','.join([str(x) for x in exchanges])
        else:
            exchangesString = exchanges

        exchangesString = exchangesString.replace(" ", "")

        if page is None:
            page = 1

        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/trades/historical?asset=' + str(asset) + "&denominator=" + str(denominator) + "&exchange=" + exchangesString + "&date=" + str(date) + "&time=" + str(time) + "&interval=" + str(interval) + "&page=" + str(page), headers=self.headers)
        return response.json()  

    """
    Gets historical OHLCV data by asset-denominator, exchange, date, time and interval.
    @param {string} asset 
    @param {string} denominator 
    @param {string/list} exchanges
    @param {string} interval 
    @param {string} dateStart
    @param {string} timeStart 
    @param {string} dateEnd
    @param {string} timeEnd 
    @param {int} page 
    Reference: https://docs.blockfacts.io/?python#ohlcv-historical-data-2
    """
    def getHistoricalOHLCVData(self, asset, denominator, exchanges, interval, dateStart, timeStart, dateEnd, timeEnd, page=None):
        exchangesString = ""

        if type(exchanges) != list and type(exchanges) != str:
            raise Exception("Parameter 'exchanges' must be of 'str' or 'list' type")

        if isinstance(exchanges, list):
            exchangesString = ','.join([str(x) for x in exchanges])
        else:
            exchangesString = exchanges

        exchangesString = exchangesString.replace(" ", "")
        
        if page is None:
            page = 1

        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/trades/ohlcv?asset=' + str(asset) + "&denominator=" + str(denominator) + "&exchange=" + exchangesString + "&interval=" + str(interval) + "&dateStart=" + str(dateStart) + "&timeStart=" + str(timeStart) + "&dateEnd=" + str(dateEnd) + "&timeEnd=" + str(timeEnd) + "&page=" + str(page), headers=self.headers)
        return response.json()  

    """
    Gets historical exchange trades in specific second.
    @param {string} asset 
    @param {string} denominator 
    @param {list/string} exchanges 
    @param {string} date 
    @param {string} time 
    Reference: https://docs.blockfacts.io/?python#specific-trade-data
    """
    def getSpecificTradeData(self, asset, denominator, exchanges, date, time):
        exchangesString = ""

        if type(exchanges) != list and type(exchanges) != str:
            raise Exception("Parameter 'exchanges' must be of 'str' or 'list' type")

        if isinstance(exchanges, list):
            exchangesString = ','.join([str(x) for x in exchanges])
        else:
            exchangesString = exchanges

        exchangesString = exchangesString.replace(" ", "")

        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/trades/specific?asset=' + str(asset) + "&denominator=" + str(denominator) + "&exchange=" + exchangesString + "&date=" + str(date) + "&time=" + str(time), headers=self.headers)
        return response.json()    

    """
    Gets the total traded volume on all exchanges by asset-denominator and interval.
    @param {string} asset
    @param {string} denominator
    @param {string} interval  
    Reference: https://docs.blockfacts.io/?python#total-trade-volume
    """
    def getTotalTradeVolume(self, asset, denominator, interval):
        response = requests.get('https://api.blockfacts.io/api/v1/exchanges/trades/total-volume?asset=' + str(asset) + "&denominator=" + str(denominator) + "&interval=" + str(interval), headers=self.headers)
        return response.json()   

    """
    Gets the moving percentage, and difference in price over a certain time period.
    @param {string} exchange 
    @param {string} denominator 
    @param {string} date 
    @param {string} interval 
    @param {string} sort 
    Reference: https://docs.blockfacts.io/?python#period-movers-2
    """
    def getPeriodMovers(self, exchange, denominator, date, interval, sort):
        response = requests.get('https://api.blockfacts.io/api/v1/blockfacts/period-movers?exchange=' + str(exchange) + "&denominator=" + str(denominator) + "&date=" + str(date) + "&interval=" + str(interval) + "&sort=" + str(sort), headers=self.headers)
        return response.json()