from .scrapper import Scrapper

class NepalStock(Scrapper):
    """
    scraps data from nepalstock.com.np
    """
    def __init__(self):
        endpoints = {
            "todayPrice":
            {
                "endpoint": "/api/nots/nepse-data/today-price",
                "parameter":{"sort":"symbol","size":500,"businessDate":""}, 
            },
            "floorsheet":
            {
                "endpoint": "/api/nots/nepse-data/floorsheet",
                "parameter":{"sort":"contractId,desc"}
            },
            "security":
            {
                "endpoint": "/api/nots/security",
                "parameter": {}
            },
            "news":
            {
                "endpoint": "/api/nots/news/media/news-and-alerts",
                "parameter": {}
            }
        }
        source = "https://newweb.nepalstock.com.np"
        super().__init__(source, endpoints)

    def getShareInfo(self):
        pass

    def getSharePrice(self,symbol,from_date=""):
        """
        get share price
        :param symbol: nepse stock symbol
        :type symbol: str
        :param from_date: get the price of specific date
        :type from_date str

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("todayPrice", businessDate=from_date)
        return self.get("todayPrice", **postData).json()

    def getFloorSheet(self):
        """
        get floor sheet

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("floorsheet")
        return self.get("floorsheet").json()

    def getSecurities(self):
        """
        get security information

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("security")
        return self.get("security").json()

    def getNews(self):
        """
        get nepse news

        :returns: list of data
        :rtype: list
        """
        postData = self.createParameter("news")
        return self.get("news").json()

