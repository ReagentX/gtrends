import sys
import pandas as pd
from pytrends.request import TrendReq
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
        status = 'normalized' if self.normalize else 'not normalized'
        return f'Lookup {self.kw}, {status}.'

    def set_normalize(self, n: bool):
        if n:
            self.normalize = True
        else:
            self.normalize = False

    # Multiprocessing
    def get(self, processes=10):
        """Handles multiprocessing using ThreadPool; sends items from a list to a function and gets the results as a list"""
        # If we want to normalize, bypass threading
        if self.normalize:
            result = self.gen_data(self.kw)
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

        # Display progress as the scraper runs its processes
        while (len(self.kw) > 1):
            completed = result._index

            # Break out of the loop if all tasks are done or if there is only one task
            if (completed == len(self.kw)):
                sys.stdout.flush()
                sys.stdout.write('\r' + "")
                sys.stdout.flush()
                break

            # Avoid a ZeroDivisionError
            if completed > 0:
                sys.stdout.flush()
                sys.stdout.write('\r' + f"{completed/len(self.kw)*100:.0f}% done. {len(self.kw)-completed} left. ")
                sys.stdout.flush()
            sys.stdout.flush()

        pool.join()

        # Result is a list of each different Pandas Dataframe, so we concatenate them together
        result = pd.concat(result, axis=1, join='inner').drop('isPartial', axis=1)

        return result

    def gen_data(self, keywords):
        '''Generate a Pandas Dataframe based on the keyword passed'''
        # Handle when we are passed a list of single letters
        if len(keywords[0]) == 1:
            keywords = [''.join(keywords)]

        if self.normalize:
            # Raise error before we send the request
            if len(keywords) > 5:
                raise ValueError('Too many keywords for normalizaion.')

            self.pytrends.build_payload(keywords, self.cat, self.tf, self.geo, self.gprop)
            data = self.pytrends.interest_over_time()
            return data
        else:
            for keyword in keywords:
                print(f'Getting {keyword}')

                # Build the dataset with the first keyword
                if keyword == keywords[0]:
                    self.pytrends.build_payload([keyword], self.cat, self.tf, self.geo, self.gprop)
                    data = self.pytrends.interest_over_time()
                    continue

                # After we have the dataset we append the new data
                self.pytrends.build_payload([keyword], self.cat, self.tf, self.geo, self.gprop)
                data[keyword] = self.pytrends.interest_over_time()[keyword]

            # Rearrange columns
            cols = list(data.columns.values)
            cols.append(cols.pop(cols.index('isPartial')))

            return data[cols]
