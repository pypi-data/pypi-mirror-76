from .scrapper import Scrapper
import datetime

class NRB(Scrapper):
    """
    scraps data from nepal rastra bank
    """
    def __init__(self):
        source = "https://www.nrb.org.np"
        endpoints = {
            "forex": {
                "endpoint": "/wp-json/wp/v2/forex",
                "parameter": {"after":"", "before":"", "order":"asc"}
            }
        }
        super().__init__(source, endpoints)

    def NRBExTable(self, from_date=datetime.datetime.now(), to_date=datetime.datetime.now()):
        """
        gets the exchange rate data

        :param from_date: date from which data should be extracted
        :type from_date: datetime
        :param to_date: date to which data should be extracted
        :type to_date: datetime

        :returns: a list of NRB Exchange Rate Data
        :rtype: list
        """
        parameters = self.createParameter("forex", after=from_date.strftime("%Y-%m-%d %T"), before=to_date.strftime("%Y-%m-%d %T"))
        response = self.get("forex", **parameters)
        return response.json()

    def NRBExData(self, currency, from_date=datetime.datetime.today() - datetime.timedelta(days=4), to_date=datetime.datetime.today()):
        """
        gets the specific exchange data
        
        :param currency: currency code
        :type currency: str
        :param info: information to be fetched
        :type info: str
        :param from_date: date of which information is to be fetched
        :type to_date: datetime

        :returns: list of data
        :rtype: list
        """
        data = self.NRBExTable(from_date, to_date)
        return list(filter(lambda d: d["currency"].lower() == currency.lower(), data[-1]["rates"]))
    
