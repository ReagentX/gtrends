from pytrends.request import TrendReq
import pandas as pd


# Connect to Google 
pytrends = TrendReq(hl='en-US', tz=360)
# Build the payload

def gen_data(keywords, normalize=True):
    if normalize: 
        pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='', gprop='')

        b = pytrends.interest_over_time()
        print(b)
    else:
        data = pd.DataFrame()
        for keyword in keywords:
            print(f'Getting {keyword}')
            pytrends.build_payload(keyword, cat=0, timeframe='today 5-y', geo='', gprop='')
            data.merge(pytrends.interest_over_time())
        print(data)


k = ['Facebook', 'Instagram']
gen_data(k, False)
