import time
import datetime
import requests

from ks_price_data import CrawlingFirmPriceData
from utils import Alert
from utils import CountDay

class StopLoss:
    def stop_loss_price(self, start_price, stop_ratio):
        return start_price * (1-stop_ratio)

    def win_price(self, start_price, win_ratio):
        return start_price * win_ratio

    def monitoring_one(self, firm_code, firm_name, start_price,
                       stop_ratio, win_ratio, buy_date, num, flags):
        price_data = CrawlingFirmPriceData('day', 1)
        try:
            firms = price_data.crawling_type_a(firm_code,firm_name)
        except requests.exceptions.Timeout:
            time.sleep(60)
            firms = price_data.crawling_type_a(firm_code,firm_name)

        stop_price = int(self.stop_loss_price(start_price, stop_ratio))
        win_price = int(self.win_price(start_price, win_ratio))
        close = int(firms.loc[0, 'close'])
        stop_ratio = round(close / stop_price, 2)
        win_ratio = round(close / win_price, 2)
        count_day = buy_date

        print('{0} monitoring {1} win:{2}/{3}-{4}, stop:{5}/{6}-{7}, buy_date:{8}, {9}'.format(
                                num, firm_code,
                                close, win_price, win_ratio,
                                close, stop_price, stop_ratio,
                                count_day, firm_name))
        print('--------------------------------------------------------------')

        if stop_price >= close:
            Alert().stop_alert(firms)
            flags[num] = 1
            return flags

        if win_price <= close:
            Alert().win_alert(firms)
            flags[num] = 1
            return flags

        return flags

    def run(self, firm_codes, firm_names, start_prices,
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
    buy_dates =    ['01-23',   '01-23',   '01-23', '01-23']
    firm_codes =   ['002360',  '037950', '083640', '215600']
    firm_names =   ['SH에너지화학', '엘컴텍', '인콘', '신라젠']
    start_prices = [1098, 1669, 1474, 15743]
    win_ratios =   [1.014, 1.014, 1.020, 1.015]
    stop_ratios =  [0.045, 0.045, 0.045, 0.045]
    flags = [0 for x in range(len(firm_codes))]

    while True:
        now = datetime.datetime.now()
        day = now.weekday()
        hour = int(now.strftime('%H'))
        if hour >= 9 and hour <= 16 and day <= 4:
            stop_loss.run(firm_codes, firm_names,
                          start_prices, stop_ratios, win_ratios,
                          buy_dates, flags)
        # stop_loss.monitoring_all(firm_codes, firm_names,
        #                          start_prices, stop_ratios, win_ratios,
        #                          buy_dates, flags)
