# This is the file where I will be practicing data manipulation alongside the Cleaning Data videos on PluralSight
# # Exercise setup/outline from https://ed.devmountain.com/materials/data-bp-1/exercises/cleaning-data/
# # Working in VS Code, tried using Jupyter Notebook extension for the first time. When I tried running some code, said no compatible kernel for Python 3.10 so needed to launch/install ipykernel? But clicked okay, everything installed, and then my code worked. Good for visualization so tested each line of code there, but larger file, so not uploading it to GitHub.

import pandas as pd

data = pd.read_csv('artwork_sample.csv')
fulldf = pd.read_csv('artwork_data.csv', low_memory=False)



###########################################
# STEP 1: UNDERSTANDING YOUR DATA
###########################################

data.columns # displays column names in a list in a tuple
data.head() # display first 5 rows
data.dtypes # lists each column + data type of each column
fulldf.dtypes # lists each column + data type of each column
# NOTE: object data types if there are bad values
fulldf.shape # returns number of (rows, columns)

data.acquisitionYear # the column as a series
data.acquisitionYear = data.acquisitionYear.astype(float) 
# .astype(float) makes a new column as that type, does not change the column in place unless set equal to this new column

fulldf.height = pd.to_numeric(fulldf.height, errors="coerce")
# converts height values to numeric, errors coerced into NaN

data.year.min() # min value for the year column
data.agg(['min', 'max']) # min row & max row for each column

height = data.height # save series from 'height' column to object
norm = (height - height.mean()) / height.std()	# standardized around 0
data['standardized_height'] = norm # create new column and add to the existing dataFrame

data.filter(items=['id','artist']) # only see those 2 columns
data.filter(like='ear') # only see LIKE columns. NOTE: case sensitive.
fulldf.filter(axis=0, regex="^100.$") # access rows 1000-1009



###########################################
# STEP 2: REMOVE AND FIX COLUMNS
###########################################
data.drop(0, inplace=True) # data.drop(labels=[0]) # drops the first row
data.drop('id', axis=1, inplace=True) # data.drop(columns=['id']) # drops that column
data = pd.read_csv('artwork_sample.csv', usecols=['artist', 'title']) # only import specified columns

data.columns # displays column names in a list in a tuple
data.columns.str.lower() # (x.lower() for x in data.columns) # map(lambda x: x.lower(), data.columns) # convert column titles to lowercase

import re
data.columns = [re.sub(r'([A-Z])', r'_\1', x).lower() for x in data.columns] # this example converts camelCase to snake_case

data.rename(columns={'thumbnailUrl': 'thumbnail'}, inplace=True) # this renames with key:value pairs, key is original name, value is new name

# Could also do data.columns, copy list of column names, make changes in that list, then data.columns = that list.



###########################################
# STEP 3: INDEX AND FILTER
###########################################
data['id'][1] # displays first value in that series
data[1:5][['artist', 'title']] # NOTE displays rows at integer position 1,2,3,4, ignores labels, & only displays specified columns

data.loc[0:2, 'title'] # displays series from that column
data.loc[0:2, :] # NOTE displays rows at label 0,1,2 & ALL columns
data.loc[[1,5], ['artist', 'title']] # displays both rows/columns as dataFrame
data.loc[0:2, 'artist':'artistId'] # displays dataFrame with all columns between
data.loc[data.artist == 'Blake, Robert', ['artist', 'title']] # only rows with that name & only specified columns in dataFrame

data.iloc[0:3, :] # NOTE displays rows at integer position 0,1,2, ignores labels
data.iloc[[5,8], [0,2]] # displays rows at integer position 5,8 and columns at integer position 0,2. Integer position is the index, not the column,so  displayed anyways

data.set_index('id', inplace=True) # so index is 'id' instead of integer position
data.iloc[0:3, :] is data.loc[1035:1037, :] # without the above line, this would return an empty dataFrame and they would not be the same

data.medium # 'medium' is a column name, this displays a series of strings, which allows us to use string methods
data.medium.str.contains('graphite|line', case=False, regex=True) # return series of True/False, case sensitive by default, and made it regex so I could use logical OR operator |
data.loc[data.medium.str.contains('graphite', na=False, case=False), ['artist','medium']]	# displays dataFrame with rows where True, only shows above 2 columns. na=False tells it to skip NA/NaN values, case=False tells it to be case insensitive.



###########################################
# STEP 4: HANDLE BAD DATA
###########################################
