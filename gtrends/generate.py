import sys
import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from multiprocessing.pool import Pool as ThreadPool


class GoogleTrendsData(object):
    '''Class to get data from Google Trends concurrently.'''
    def __init__(self, kw: list, normalize: bool, category='', timezone=0, timeframe='', geo='', gprop=''):
        self.kw = kw
        self.normalize = normalize
        self.cat = category
        self.tf = timeframe
        self.geo = geo
        self.gprop = gprop
        self.pytrends = TrendReq(hl='en-US', tz=timezone)

    def __repr__(self):
        return f'Lookup {self.kw}, {"normalized" if self.normalize else "not normalized"}.'

    def set_normalize(self, n: bool):
        if n:
            self.normalize = True
        else:
            self.normalize = False

    # Multiprocessing
    def get(self, processes=10):
        """Handles multiprocessing using ThreadPool; sends items from a list to a function and gets the results as a list"""
        # If we already have the data, get it from the CSV file without talking to Google
        file_name = 'output/' + ''.join(self.kw) + ('Normalized' if self.normalize else 'NotNormalized') + '.csv'

        try:
            data = pd.read_csv(file_name)
            print('Data cached. Reading csv...')
            # Convert the date column from str to datetime
            data['date'] = pd.to_datetime(data['date'])
            return data
        except FileNotFoundError:
            print('Cache miss')
            pass

        # If we want to normalize, bypass threading
        if self.normalize:
            result = self.gen_data(self.kw)

            # If we get an array back instead of a DataFrame we are rate limited
            try: 
                result.drop('isPartial', axis=1)
            except AttributeError:
                sys.exit('Rate limited.')

            return result.drop('isPartial', axis=1)

        # Define the number of processes, use less than or equal to the defined value
        count_threads = min(processes, len(self.kw))
        if count_threads == 0:
                return []
        pool = ThreadPool(count_threads)

        # Tell the user what is happening
        print(f"Getting {len(self.kw)} items in {count_threads} processes.")

        # Calls gen_data() and adds the filesize returned each call to an self.kw
        result = (pool.imap_unordered(self.gen_data, self.kw))
        pool.close()
        pool.join()

        # Result is a list of each different Pandas Dataframe, so we concatenate them together
        try:
            result = pd.concat(result, axis=1, join='inner').drop('isPartial', axis=1)
        except TypeError:
            sys.exit('Rate limited.')

        return result

    def gen_data(self, keywords):
        '''Generate a Pandas Dataframe based on the keyword(s) passed'''
        # Handle when we are passed a list of single letters
        if len(keywords[0]) == 1:
            keywords = [''.join(keywords)]

        if self.normalize:
            # Raise error before we send the request
            if len(keywords) > 5:
                raise ValueError('Too many keywords for normalizaion.')

            try:
                self.pytrends.build_payload(keywords, self.cat, self.tf, self.geo, self.gprop)
            except ResponseError:
                return []

            data = self.pytrends.interest_over_time()
            return data

        # Handle when we are not normalizing the data
        else:
            for keyword in keywords:
                print(f'Getting {keyword}')

                # Build the dataset with the first keyword
                if keyword == keywords[0]:
                    try:
                        self.pytrends.build_payload([keyword], self.cat, self.tf, self.geo, self.gprop)
                    except ResponseError:
                        return []

                    data = self.pytrends.interest_over_time()
                    continue

                # After we have the dataset we append the new data
                self.pytrends.build_payload([keyword], self.cat, self.tf, self.geo, self.gprop)
                data[keyword] = self.pytrends.interest_over_time()[keyword]

            # Rearrange columns
            cols = list(data.columns.values)
            cols.append(cols.pop(cols.index('isPartial')))

            return data[cols]

    def graph(self, data, filename='o'):
        p = data.plot(x='date')
        p.set_title(f'Interest Over Time: {"Normalized" if self.normalize else "Not Normalized"}')
        p.set_ylabel('Interest Level')
        p.set_xlabel('Date')
        p.get_figure().savefig(f'{filename}.png')
        return p

    def save(self, d):
        d.to_csv(f'./output/{"".join(self.kw)}{"Normalized" if self.normalize else "NotNormalized"}.csv', index=False)
