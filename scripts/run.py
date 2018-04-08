import pandas as pd
from gtrends import generate

# Criteria
keywords = ['Facebook', 'Instagram', 'Twitter', 'Google Plus', 'Reddit']
normalize = False

# Generate the data
data = generate.gen_data(keywords, normalize)
print(data.head())

# Dump to a CSV file
data.to_csv(f'./output/{"".join(keywords)}.csv')
