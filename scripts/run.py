import pandas as pd
from gtrends import generate

# Required object properties
keywords = ['Facebook', 'Instagram', 'Twitter', 'Google Plus', 'Reddit']
normalize = True

# These are optional and may be omitted from construction
category = 0  # https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
geo = ''  # Empty is world, use 2-letter ISO code
timezone = 480  # 480 for PST, timezone offset in minutes
timeframe = 'today 5-y'  # See `timeframe` under https://github.com/GeneralMills/pytrends#common-api-parameters
gprop = ''  # Empty is "Web search", see above link

# Generate the object that will normalize the data
gt = generate.GoogleTrendsData(keywords, normalize, timezone=timezone, geo='US')

# Print the request info
print(gt)

# Generate the data
data = gt.get(processes=5)

# Dump to a CSV file
gt.save(data)
gt.graph(data)
