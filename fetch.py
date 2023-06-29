import json
import requests

ticker = "SNOW"
option_dates = ['2023-06-01', '2023-06-02', '2023-06-03', '2023-06-04']
expiration_date = '2023-07-14'


def get_data(end_point):
    response = requests.get(end_point)
    response_data = json.loads(response.text)
    return response_data


for option_date in option_dates:
    endpoint = f"https://api-v2.intrinio.com/options/chain/{ticker}/{expiration_date}/eod?date={option_date}&api_key" \
           ""
    print(endpoint)
    # endpoint = "https://api-v2.intrinio.com/options/chain/SNOW/2023-07-14/eod?date=2023-06-01&api_key=OjEyOTNmNGRkOGE5ODk2MjllNjg5N2FlNjA0N2Y4YjRm"
    data = get_data(endpoint)

    with open(f'{ticker}_{option_date}_{expiration_date}.json', 'w')as f:
        json.dump(data, f)
