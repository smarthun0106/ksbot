import requests
import inspect

class Alert:
    def __init__(self):
        self.TELEGRAM_ERROR_BOT_TOKEN = "929204433:AAHo8Z8SRIXrit0IBQ85JEWXoHjCwu0WbVM"
        self.TELEGRAM_REPORT_BOT_TOKEN = "827588378:AAF4OPFPzDGHuAKY47YIp68H4Fp68I6xoTM"

    def telegram_url_path(self, token):
        url = "https://api.telegram.org"
        path = "/bot{0}/sendMessage".format(token)
        url_path = url + path
        return url_path

    def telegram_text(self, text):
        token = self.TELEGRAM_REPORT_BOT_TOKEN
        url_path = self.telegram_url_path(token)
        parameters = { "chat_id" : "756052880", "text" : text }
        r = requests.get(url_path, params=parameters)
        return r

    '''
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return:
    '''
    def retrieve_name(self, var):
        for fi in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]

    def stretagy_alert(self, stretagy):
        stretagy_name = self.retrieve_name(stretagy).upper()
        if len(stretagy.index) > 0:
            for num, code in enumerate(stretagy.index):
                text = stretagy_name + ': ' +  stretagy.loc[code, 'name'] + ' ' + code
                self.telegram_text(text)
        else:
            text = stretagy_name + ': ' + 'No Data'
            self.telegram_text(text)

    def stop_alert(self, df):
        code = df.loc[0, 'code']
        name = df.loc[0, 'name']
        text = 'Stop: ' + code + ' ' + name
        self.telegram_text(text)