import pandas as pd
from gtrends import generate

# Object properties
keywords = ['Facebook', 'Instagram', 'Twitter', 'Google Plus', 'Reddit']
normalize = False
category = 0  # https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
geo = ''  # Empty is world, use 2-letter ISO code
timezone = 480  # 480 for PST, timezone offset in minutes
timeframe = 'all'  # See `timeframe` under https://github.com/GeneralMills/pytrends#common-api-parameters
gprop = ''  # Empty is "Web search", see above link

# Generate the object that will normalize the data
gt = generate.GoogleTrendsData(keywords, normalize, category, timezone, timeframe, geo, gprop)

# Print the status of the request
# gt.set_normalize(False)
print(gt)

# Generate the data
data = gt.get()
print(data.head())

# Dump to a CSV file
# data.to_csv(f'./output/{"".join(keywords)}.csv')
