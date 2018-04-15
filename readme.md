# gtrends: A Google Trends Analytics Package

Inspired by [this reddit post](https://www.reddit.com/r/dataisbeautiful/comments/8ahy05/internet_communities_popularity_on_google_trends/), I wanted to build a simple platform to pull data from Google Trends. The author made the interesting choice not to normalize the data (i.e., that the value of popularity does not represent the same amount of search volume across each category). 

While this means that it _does not_ compare the actual popularity of the social networks, it _does_ elucidate where the networks' popularity happens to spike in the context of other networks' popularity. I built in an option that allows you to specify whether to normalize or not.

The `get()` function is multiprocessed, thus multiple keywords will be handled concurrently to speed up data collection routines. The number of processes depends on the number of keywords passed, however, Google may rate limit overly ambitious requests. The script checks if the requested data already exists in the output folder before making new queries.

## Normalized

![Normalized](https://i.imgur.com/AU0c7fu.png)

## Not Normalized

![Not Normalized](https://i.imgur.com/120geGD.png)

## Usage

For an example on how to use this script see `run.py` in the `scripts` folder. In short, define a list of keywords:

    keywords = ['Facebook', 'Instagram', 'Twitter', 'Google Plus', 'Reddit']

Determine if you want to normalize:

    normalize = False

Generate a GoogleTrendsData object:

    gt = generate.GoogleTrendsData(keywords, normalize)

Run `gt.get()`:

    data = gt.get()

This will return a Pandas DataFrame. Happy analyzing!

### Built-in Functions

    gt.save(data)

Will export the data to a CSV file. This is useful because the script checks the output folder before making new queries, thus reducing the likelihood of hitting the rate limit.

    gt.grapgh(data, file_name)

Will save an image of the line graph using `pandas.plot()`.

***

## Notes

- Google only allows you to normalize up to five keywords at once. Trying to normalize more than 5 keywords will raise a `ValueError`.
- Google may rate limit you if you make too many requests which can lead to `TypeError`s or `ResponseError`s.
- This package is dependent on [`pandas`](https://pandas.pydata.org/) and [`pytrends`](https://github.com/GeneralMills/pytrends) which can be installed via pip.