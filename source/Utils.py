import requests
import inspect
import random
import datetime

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
    Gets the name of var.
    Does it from the out most frame inner-wards.
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

    def win_alert(self, df):
        code = df.loc[0, 'code']
        name = df.loc[0, 'name']
        text = 'Win: ' + code + ' ' + name
        self.telegram_text(text)

class CountDay:
    def __init__(self):
        self.today = datetime.datetime.now()

    def count(self, date):
        year = int(self.today.strftime('%Y'))
        month = int(date[:2])
        day = int(date[3:5])
        set_date = datetime.datetime(year, month, day)
        today = datetime.datetime.now()
        count_d = today - set_date
        return count_d.days



class Key:

	def __init__(self, key=''):

		if key == '':
			self.key= self.generate()
		else:
			self.key = key.lower()

	def verify(self):
		score = 0
		check_digit = self.key[0]
		check_digit_count = 0
		chunks = self.key.split('-')
		for chunk in chunks:
			if len(chunk) != 4:
				return False
			for char in chunk:
				if char == check_digit:
					check_digit_count += 1
				score += ord(char)
		if score == 1772 and check_digit_count == 5:
			return True
		return False

	def generate(self):
		key = ''
		chunk = ''
		check_digit_count = 0
		alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
		while True:
			while len(key) < 25:
				char = random.choice(alphabet)
				key += char
				chunk += char
				if len(chunk) == 4:
					key += '-'
					chunk = ''
			key = key[:-1]
			if Key(key).verify():
				return key
			else:
				key = ''

	def __str__(self):
		valid = 'Invalid'
		if self.verify():
			valid = 'Valid'
		return self.key.upper() + ':' + valid

if __name__ == "__main__":
    count_day = CountDay()
    day = count_day.count('01-20')
    print(day)
