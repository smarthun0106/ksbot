import time
import datetime
import requests

from KsDataFrame import PriceData
from Utils import Alert

class StopLoss:
    def stop_loss_price(self, start_price, stop_ratio):
        return start_price * (1-stop_ratio)

    def monitoring_one(self, firm_code, firm_name, start_price,
                       stop_ratio, num, flags):
        try:
            stop_firms = PriceData().price_data_a(firm_code, firm_name, 'day', 1)
        except requests.exceptions.Timeout:
            time.sleep(60)
            stop_firms = PriceData().price_data_a(firm_code, firm_name, 'day', 1)

        stop_price = self.stop_loss_price(start_price, stop_ratio)
        close = int(stop_firms.loc[0, 'close'])
        result = round(int(close) / int(stop_price), 4)
        print('{0} monitoring {1} {2}, {3}'.format(num, firm_code, firm_name, result))
        if stop_price >= close:
            Alert().stop_alert(stop_firms)
            flags[num] = 1
            return flags
        return flags

    def monitoring_all(self, firm_codes, firm_names, start_prices,
                       stop_ratios, flags):
        for num, firm_code in enumerate(firm_codes):
            if flags[num] != 1:
                time.sleep(1)
                flags = self.monitoring_one(firm_code, firm_names[num],
                                            start_prices[num], stop_ratios[num],
                                            num, flags)


if __name__ == "__main__":
    stop_loss = StopLoss()
    firm_codes = ['007110', '078130']
    firm_names = ['일신석재', '국일제지']
    start_prices = [2622, 5910]
    stop_ratios = [0.04, 0.04]
    flags = [0 for x in range(len(firm_codes))]

    while True:
        time.sleep(1)
        now = datetime.datetime.now()
        day = now.weekday()
        hour = int(now.strftime('%H'))
        if hour >= 9 and hour <= 16 and day <= 5:
            stop_loss.monitoring_all(firm_codes, firm_names, start_prices, stop_ratios, flags)
