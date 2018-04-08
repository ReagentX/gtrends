import pandas as pd
from gtrends import generate


keywords = ['Facebook', 'Instagram', 'Twitter', 'Snapchat', 'Google Plus', 'Reddit']
data = generate.gen_data(keywords, False)
print(data.head())

# Dump to a CSV file
data.to_csv(f'./output/{"".join(keywords)}.csv')
