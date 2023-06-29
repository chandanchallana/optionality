import json
import os


class Option:
    def __init__(self, option_type, strike, expiration_date, current_date, volume, open_interest, delta, gamma, iv,
                 close):
        self.option_type = option_type
        self.strike = strike
        self.expiration_date = expiration_date
        self.volume = volume or 0
        self.open_interest = open_interest or 0
        self.delta = delta
        self.current_date = current_date
        self.gamma = gamma
        self.iv = iv
        self.close = close

    def __str__(self):
        return f"{self.option_type} {self.strike} {self.expiration_date} " \
               f"{self.current_date} {self.volume} {self.open_interest} {self.close}"


def get_file_names_for_dir(dir_name):
    option_file_names = []
    for filename in os.listdir(dir_name):
        if os.path.isfile(os.path.join(dir_name, filename)):
            option_file_names.append(filename)
    return option_file_names

file_names = get_file_names_for_dir('./SNOW')

print("Type strike exp_date volume open_interest delta")
strikes_and_vols = []
for file_name in file_names:
    opt_dict = {}
    with open(f'./SNOW/{file_name}') as f:
        data = json.load(f)
        for option in data['chain']:
            option_type = option['option']['type']
            strike = option['option']['strike']
            exp_date = option['option']['expiration']
            if 'price' in option:
                key = 'price'
            else:
                key = 'prices'
            volume = option[key]['volume']
            open_interest = option[key]['open_interest']
            delta = option[key]['delta']
            close = option[key]['close']
            current_date = option[key]['date']
            try:
                gamma = option[key]['gamma']
            except:
                gamma = 0
            iv = option[key]['implied_volatility']
            strike_str = str(strike)
            if strike_str not in opt_dict:
                options = []
                option_data = Option(option_type, strike, exp_date, current_date, volume, open_interest, delta,
                                     gamma, iv, close)
                options.append(option_data)
                opt_dict[strike_str] = options
            else:
                options = opt_dict[strike_str]
                options.append(Option(option_type, strike, exp_date, current_date, volume, open_interest, delta,
                                      gamma, iv, close))
                opt_dict[strike_str] = options


    for key, value in opt_dict.items():

        for elem in opt_dict[key]:
            if elem.option_type == 'call' and elem.current_date == '2023-06-21' and elem.expiration_date == \
                    '2023-06-23'\
                    and elem.strike > 160 and elem.strike <= 190:
                dollarAmount = elem.delta*elem.open_interest*100
                # print(f"{elem.strike}, {elem.iv}")
                strike_and_iv = (elem.strike, elem.iv)
                strikes_and_vols.append(strike_and_iv)

sorted_strikes = sorted(strikes_and_vols)
# print(sorted_strikes)
for sorted_strike in sorted_strikes:
    print(f"{sorted_strike[0]},{sorted_strike[1]}")