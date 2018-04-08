from pytrends.request import TrendReq
import pandas as pd


# Connect to Google 
pytrends = TrendReq(hl='en-US', tz=360)

def gen_data(keywords, normalize=True):
        pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='', gprop='')
        data = pytrends.interest_over_time()
        return data
    else:
        for keyword in keywords:
            print(f'Getting {keyword}')
            if keyword == keywords[0]:
                pytrends.build_payload([keyword], cat=0, timeframe='today 5-y', geo='', gprop='')
                data = pytrends.interest_over_time()
                continue
            pytrends.build_payload([keyword], cat=0, timeframe='today 5-y', geo='', gprop='')
            data[keyword] = pytrends.interest_over_time()[keyword]
        # Rearrange columns
        cols = list(data.columns.values)
        cols.append(cols.pop(cols.index('isPartial')))
        return data[cols]


k = ['Facebook', 'Instagram', 'Twitter', 'Snapchat', 'Pinterest', 'Google', 'Reddit']
d = gen_data(k, False)
print(d)
