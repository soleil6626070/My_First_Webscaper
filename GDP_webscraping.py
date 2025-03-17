# Code no longer working as of 16th of March 2025.
# Wikipedia removed column of interest & reformatted table
# Raw data was foolishly not saved to file.

# This program is a simple webscraping exercise. I will extract some data
# from a table on wikipedia & then perform some simple manipulations for fun.

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'

#extract table data, select only the relevant table
tables = pd.read_html(URL)
df = tables[2]

#replace column names with numbers
df.columns = range(df.shape[1])

#keep only name of country, region & gdp of country quoted by IMF columns
df = df[[0,1,2]]

#rename columns
df.columns = ['Country','Continent','GDP (Million USD)']

# Because Wikipedia is editable, someone might add an empty row (as has just happened)
# I need to make sure empty rows are deleted

# Identifying NaN values with boolean indexing:
print(df[df['GDP (Million USD)'].isnull()])
#Then remove all NaN values
df = df.dropna(subset=['GDP (Million USD)'])

#Need to search data frame for countries with no IMF GDP data, to be able to exclude them.
excluded_countries = []
for i in range(213):
    if df.iloc[i, 2] == '—':
        excluded_countries.append(df.iloc[i,0])
print('The following countries were excluded from calculations due to missing data:', excluded_countries)

#create new data frame without excluded countries
# when it does not include '-', we keep it
df_clean = df[df['GDP (Million USD)'] != '—']

#change the data type of the gdp column to integer
# NOTE: using .loc[row,column] here to avoid SettingWithCopyWarning
df_clean.loc[:,'GDP (Million USD)'] = df_clean['GDP (Million USD)'].astype(int)


#change the units from millions to billions, round to 2dp
df_clean.loc[:,'GDP (Million USD)'] = df_clean[['GDP (Million USD)']]/1000
df_clean.loc[:,'GDP (Million USD)'] = np.round(df_clean[['GDP (Million USD)']] , decimals=2)
#rename the column to billions
df_clean = df_clean.rename(columns = {'GDP (Million USD)' : 'GDP (Billion USD)'})

# Now find the top 10 GDPs
#keep only the top 10 countries(rows)
df_T10 = df_clean.iloc[1:11]

#put this data frame into a csv file so it can be looked at in excel
df_T10.to_csv('./watch_mojo_top_ten_economies.csv')

print(df_T10)

#Remove the first row which just shows the gdp of the world
df_clean = df_clean.drop(0)

# Now that the data is clean, we can begin to process it for analysis
# I'd like to split the data into regions, then calculate averages

avg_GDP = df_clean.groupby('Continent')['GDP (Billion USD)'].mean()

#If we want to convert the series avg_GDP into a DataFrame we can by:
#df_region = pd.DataFrame({'Region':avg_GDP.index, 'GDP (Billion USD)':avg_GDP.values})
#print(df_region)

#------------------Graphing --------------------

avg_GDP.plot(kind='bar', color='blue')
#Title
plt.title('Average GDP (Billion USD) projected by the International Monetary Fund for 2023 by region.')

#Labels
plt.xlabel('Region')
bar_labels = ['Africa','Americas','Asia','Europe','Oceania']
plt.xticks(rotation='horizontal') #rotate xlabels for legibility
plt.ylabel('Average GDP (Billion USD)')

#Value labels
#convert series values to lists & plot them at the top of each bar
region_list = avg_GDP.index.tolist()
gdp_list = np.round( avg_GDP.values.tolist(), decimals=2)

def add_value_label(x_list, y_list):
    for i in range(1, len(x_list) + 1):
        plt.text(i-1, y_list[i - 1]+0.9, y_list[i - 1], ha="center")
        #plt.text(x-coordinate, y, s)
add_value_label(region_list, gdp_list)

plt.tight_layout()

plt.show()
