# gtrends: A Google Trends Analytics Platform

Inspired by [this reddit post](https://www.reddit.com/r/dataisbeautiful/comments/8ahy05/internet_communities_popularity_on_google_trends/), I wanted to build a simple platform to pull data from Google Trends. The author made the interesting choice to not normalzie the data (i.e., that the value of popularity does not represent the same amout of search volume across each category). 

While this means that it _does not_ compare the actual popularity of the social networks, it _does_ elicudate where the networks' popularity happens to spike in the context of other networks' popularity. I built in an option that allows you to specify whether to normalize or not.

## Normalized
![](https://i.imgur.com/AU0c7fu.png)

## Not Normalized
![](https://i.imgur.com/120geGD.png)

For an example on how to use this script see `run.py` in the `scripts` folder. In short, define a list of keywords:

    keywords = ['Facebook', 'Instagram', 'Twitter', 'Google Plus', 'Reddit']

Determine whether you want to normalize the data or not:

    normalize = False

Run `gen_data()` with the arguments above.

    data = generate.gen_data(keywords, normalize)

Happy analyzing!

***

## Notes

- Google only allows you to normalize up to 5 keywords at once. Trying to normalize more than 5 keywords will raise a `ValueError`.
- This package is dependent on [`pytrends`](https://github.com/GeneralMills/pytrends) which can be installed via pip.