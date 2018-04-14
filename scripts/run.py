import pandas as pd
from gtrends import generate

# Criteria
keywords = ['Facebook', 'Instagram', 'Twitter', 'Google Plus', 'Reddit']
gt = generate.GoogleTrendsData(keywords, True)

# Generate the data
data = gt.get()
print(data)

# Dump to a CSV file
# data.to_csv(f'./output/{"".join(keywords)}.csv')
