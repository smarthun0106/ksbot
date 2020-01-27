import time
import datetime
import requests

from KsDataFrame import PriceData
from Utils import Alert
from Utils import CountDay

class StopLoss:
    def stop_loss_price(self, start_price, stop_ratio):
        return start_price * (1-stop_ratio)

    def win_price(self, start_price, win_ratio):
        return start_price * win_ratio

    def monitoring_one(self, firm_code, firm_name, start_price,
                       stop_ratio, win_ratio, buy_date, num, flags):
        try:
            firms = PriceData().price_data_a(firm_code, firm_name, 'day', 1)
        except requests.exceptions.Timeout:
            time.sleep(60)
            firms = PriceData().price_data_a(firm_code, firm_name, 'day', 1)

        stop_price = int(self.stop_loss_price(start_price, stop_ratio))
        win_price = int(self.win_price(start_price, win_ratio))
        close = int(firms.loc[0, 'close'])
        stop_ratio = round(close / stop_price, 2)
        win_ratio = round(close / win_price, 2)
        count_day = '+' + str(CountDay().count_day(buy_date))

        print('{0} monitoring {1} win:{2}/{3}-{4}, stop:{5}/{6}-{7}, day:{8}, {9}'.format(
                                num, firm_code,
                                close, win_price, win_ratio,
                                close, stop_price, stop_ratio,
                                count_day, firm_name))

        if stop_price >= close:
            Alert().stop_alert(firms)
            flags[num] = 1
            return flags

        if win_price <= close:
            Alert().win_alert(firms)
            flags[num] = 1
            return flags

        return flags

    def monitoring_all(self, firm_codes, firm_names, start_prices,
                       stop_ratios, win_ratios, buy_dates, flags):
        for num, firm_code in enumerate(firm_codes):
            if flags[num] != 1:
                time.sleep(2)
                flags = self.monitoring_one(firm_code, firm_names[num],
                                            start_prices[num], stop_ratios[num],
                                            win_ratios[num], buy_dates[num],
                                            num, flags)


if __name__ == "__main__":
    stop_loss = StopLoss()
    buy_dates =    ['01-16',   '01-20',   '01-20']
    firm_codes =   ['078130',  '007460', '038620']
    firm_names =   ['국일제지', '에이프로젠', '위즈코프']
    start_prices = [5910, 2732, 1228]
    win_ratios =   [1.02, 1.02, 1.02]
    stop_ratios =  [0.047, 0.047, 0.047]
    flags = [0 for x in range(len(firm_codes))]

    while True:
        now = datetime.datetime.now()
        day = now.weekday()
        hour = int(now.strftime('%H'))
        if hour >= 9 and hour <= 16 and day <= 4:
            stop_loss.monitoring_all(firm_codes, firm_names,
                                     start_prices, stop_ratios, win_ratios,
                                     flags)
        # stop_loss.monitoring_all(firm_codes, firm_names,
        #                          start_prices, stop_ratios, win_ratios,
        #                          buy_dates, flags)
