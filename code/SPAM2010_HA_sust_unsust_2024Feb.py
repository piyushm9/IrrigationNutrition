# -*- coding: utf-8 -*-
"""
Feb13,2024, Piyush Mehta , Paper2 - Irrigation Nutrition

1. Import SPAM 2010 data from DHS_SPAM2010_Feb2024.xlsx
2. Merge with All_data_v3.dta after removing duplicates
3. Keep only the obs that are in All_data_v3 based on dhsid
4. Calculate fractional HA
5. Total frac HA per country would be the sum of frac HA for the DHS clusters within that country
[not using number of DHS clusters/country as weights]

folder = D:\Delaware\Work\Paper2_Irrigation_Nutrition\Data\Crop_mixes\MAP_SPAM\Total_HA_2010

"""
#%%
# CELL 1
import os
import pandas as pd
import numpy as np

# Set the option to display all columns
pd.set_option('display.max_columns', None)
# to reset it to 10 columns, use this
pd.set_option('display.max_columns', 10)

path = "D:\\Delaware\\Work\\Paper2_Irrigation_Nutrition\\Data\\Crop_mixes\\MAP_SPAM\Total_HA_2010\\"
os.chdir(path)

# Read the SPAM 2010 data file DHS_SPAM2010_Feb2024.xlsx
df = pd.read_excel(path+"Data\\DHS_SPAM2010_Feb2024.xlsx", sheet_name= "DHS_SPAM2010_Feb2024")

# Load All_data_v3.dta data
df_v3 = pd.read_stata("D:\\Delaware\\Work\\Paper2_Irrigation_Nutrition\\Data\\Combined_Data\\All_data_v3.dta")

# SPAM 2010 data has all 41 crops in it
# we only need to keep 33 crop columns
crops_spam2010 = ['cnut', 'coco', 'cott', 'oilp', 'ooil', 'rape', 'rcof', 'sesa', 'soyb', 'sugc', 'sunf', 'teas', 'bana', 'barl', 'bean', 'cass', 'grou', 'maiz', 'ocer', 'opul', 'orts',  'plnt', 'pmil', 'pota', 'rice', 'smil', 'sorg', 'swpo', 'temf', 'trof', 'vege', 'whea', 'yams']

# Specify the columns to select
selected_columns = ['DHSID', 'URBAN_RURA', 'Country', 'DHSYEAR'] + [col for col in df.columns if any(crop_name in col for crop_name in crops_spam2010)]
# Select the specified columns
df = df[selected_columns]

#%%
# CELL 2
# Keep only rural clusters
# Replace nan cells with 0 in df1
# THIS IS NEEDED, AS I WAS NOT GETTING THE SUM OF FRACTIONAL VARS AS 1 BEFORE DOING THIS
df1 = df[df['URBAN_RURA'] == "R"].fillna(0)
df_v3 = df_v3[df_v3['URBAN_RURA'] == "R"]

# Rename the variable 'DHSID' to 'dhsid' and Drop duplicates based on 'dhsid' variable
df1.rename(columns={'DHSID': 'dhsid'}, inplace=True)
df1 = df1.drop_duplicates(subset='dhsid')

# Only keep the observations matching with the All_data_v3.dta dataset
# Merge based on 'dhsid'
df2 = pd.merge(df1, df_v3, on='dhsid', how='inner')
# left with 9181 observations, equal to what is in All_data_v3.dta file

#check the URBAN_RURA variable values after merging
df2['URBAN_RURA_x'].value_counts()
#df2['region'].value_counts()

#%%
# CELL 3
# get the columns ending with 2000 or 2010 (we need 41 crop columns)
filtered_columns = df2.filter(regex=r'(2000|2010)$')
# remove aei columns that also end with 2000/2010
filtered_columns=filtered_columns.drop(columns=['aei2000','aei2010','aei_pct2000','popden2000','popden2010']) #41 left (41 crops)
# Convert the column names to a list
crops_columns = filtered_columns.columns.tolist()
# List of columns to keep
columns_to_keep = ['dhsid', 'Country_x', 'DHSYEAR', 'URBAN_RURA_x',  'aei_sust']+ crops_columns
# Keep only the specified columns in df2
df3 = df2[columns_to_keep]

# Rename a few columns
df3.rename(columns={'URBAN_RURA_x': 'urban_rural'}, inplace=True)
df3.rename(columns={'DHSYEAR': 'dhsyear'}, inplace=True)
df3.rename(columns={'Country_x': 'country'}, inplace=True)

# check country names in df3
df3['country'].unique()
# rename country from Congo Democratic Republic to Congo in df3
df3['country'] = df3['country'].replace('Congo Democratic Republic', 'Congo')
df3['country'].unique()

#%%
# CELL 4 [was part of cell 6]
## Calc the sum of HA for each crop for each country
## Take the sum of the HA for each crop for all DHS clusters within a country
# so that we have each row as the total HA for each crop per country 

# Keep only crop columns
crop_columns = ['country','aei_sust'] + [col for col in df3.columns if col.endswith('2000') or col.endswith('2010')]
df4_0 = df3[crop_columns] 

# Collapse data to country level for 2010 by taking the sum 
# Group by 'country' & aei_sust and calculate the sum of all crop variables
df4 = df4_0.groupby(['country', 'aei_sust']).sum().reset_index()

# calc tot_HA2010  vars for 41 crops
#  crops excluding cash & nutri
crops2010 = [item for item in crops_columns if item.endswith("2010")]

df4['tot_HA2010']= df4[crops2010].sum(axis=1)

# Adding this tot_HA2000 column in df3 as well as we will need it later
df3['tot_HA2010']= df3[crops2010].sum(axis=1)


#%%
# CELL 5
# Calculate fractional HA for each country
# (1) 2010
# Create a new DataFrame for fractional HA for 2010
df4_2010_fractional = df4[crops2010].div(df4['tot_HA2010'], axis=0)
# Rename the fractional columns
df4_2010_fractional.columns = [f'{col}_f' for col in crops2010]

# make a new df to store this info
df5 = df4_2010_fractional.copy()

# order vars
df4_frac_columns = [col for col in df5.columns if col.endswith('_f')] # 41 columns

# take cols country and aei_sust from df4, and merge it with df5 
df5 = pd.concat([df4[['country', 'aei_sust']], df5], axis=1)
# Now df5 has country, aei_sust and 41 fractional crop HAs

# fractional crops excluding cash & nutri
crops_f2010 = [col for col in df5.columns if col.endswith('2010_f')]

#export to check the sum of frac columns
#df5.to_csv(path+'df5.csv', index=False) 
# looks good , sum = 1 for both 2000 and 2020 crops [feb13,24]

#%%
# CELL 6
# CALCULATE CASH AND NUTRITIONAL FRACTIONAL HA FOR EACH COUNTRY
# Using the tot_HA2010 var made in the prev cells

# cash crops 12
cash = ['cnut', 'coco', 'cott', 'oilp', 'ooil', 'rape', 'rcof', 'sesa', 'soyb', 'sugc', 'sunf', 'teas']
# nutri crops 21
nutri = ['bana', 'barl', 'bean', 'cass', 'grou', 'maiz', 'ocer', 'opul', 'orts',  'plnt', 'pmil', 'pota', 'rice', 'smil', 'sorg', 'swpo', 'temf', 'trof', 'vege', 'whea', 'yams']

# Add "2010" to each element in the lists, save as new list
cash_2010 = [crop + "2010" for crop in cash] #16 crops
nutri_2010 = [crop + "2010" for crop in nutri] #25 crops

# (1) 2010
# Create the 'cash2010' and 'nutri2010' column by summing the resp crop columns
df3['cash2010'] = df3[cash_2010].sum(axis=1)
df3['nutri2010'] = df3[nutri_2010].sum(axis=1)

# Check if the sum of cash2010 and nutri2010 equals tot_HA2010
df3_test = df3[['cash2010','nutri2010','tot_HA2010']]
del df3_test # remove this df

# Make a separate dataframe for cash nutri vars
df3_cash_nutri = df3[['country', 'aei_sust', 'cash2010','nutri2010','tot_HA2010']]

# Take sum and collapse at country and aei_sust level
df4_cash_nutri = df3_cash_nutri.groupby(['country', 'aei_sust']).sum().reset_index()

# calc fractional HA for 2000
df4_cash_nutri['cash2010_f'] = df4_cash_nutri['cash2010']/df4_cash_nutri['tot_HA2010']
df4_cash_nutri['nutri2010_f'] = df4_cash_nutri['nutri2010']/df4_cash_nutri['tot_HA2010']

# export df4_cash_nutri (test)
#df4_cash_nutri.to_csv(path+'df4_cash_nutri.csv', index=False) 

# keep only cash nutri frac columns
df4_cash_nutri_frac_columns = [col for col in df4_cash_nutri.columns if col.endswith('_f')] # 4
df4_cash_nutri1 = df4_cash_nutri[df4_cash_nutri_frac_columns]

# combine these cash nutri frac HA columns with df5 that has each crops fractional HAs
df5 = pd.concat([df5, df4_cash_nutri1],  axis=1)

# THIS DF5 HAS THE FRACTIONAL HA FOR EACH CROP AT COUNTRY & SUST LEVEL
# ALSO CONTAINS THE FRACTIONAL HA FOR CASH AND NUTRITIONAL CROPS

# The following countries don't have data for both sust and unsust clusters, so I will drop them
# Angola, Benin, Congo, Ghana, Guinea, Lesotho, Liberia, Rwanda, Uganda
countries_to_drop = ['Angola', 'Benin', 'Congo', 'Ghana', 'Guinea', 'Lesotho', 'Liberia', 'Rwanda', 'Uganda']
df5 = df5[~df5['country'].isin(countries_to_drop)]

# NOW DF5 ONLY HAS 17 COUNTRIES DATA

#sample size
# df3_counts = df3.groupby('aei_sust').size().reset_index(name='count')
# 5902 observations for sustainable, 3279 obs for unsustainable


#%%
# CELL 7
# WE NEED THIS RN, BUT I WILL FOR REGIONAL PART [Feb1,24]

# adding region variable
df5['region'] = ''
# Specify the columns for which we want to calculate the average
america = ["Haiti", "Peru"]
asia = ["Bangladesh", "Cambodia", "Nepal", "Philippines"]
middle_east = ["Egypt", "Jordan"] # Congo Democratic Republic is Congo
southeast_africa = ["Angola", "Congo", "Ethiopia", "Kenya", "Lesotho", "Madagascar", "Malawi", "Rwanda", "Tanzania", "Uganda", "Zimbabwe"]
west_africa = ["Benin", "Cameroon", "Ghana", "Guinea", "Liberia", "Mali", "Nigeria"]
# Replace 'region' values based on conditions
df5.loc[df5['country'].isin(america), 'region'] = 'America'
df5.loc[df5['country'].isin(asia), 'region'] = 'Asia'
df5.loc[df5['country'].isin(middle_east), 'region'] = 'Middle East'
df5.loc[df5['country'].isin(southeast_africa), 'region'] = 'Southern/East Africa'
df5.loc[df5['country'].isin(west_africa), 'region'] = 'West Africa'

# all frac columns including cash vs nutri
frac_columns1 = [col for col in df5.columns if col.endswith('_f')]
#a = ['region', 'country', 'country_count']+frac_columns1
# order vars, keep cash nutri columns at the end
df5 = df5[['region', 'country', 'aei_sust' ]+frac_columns1]
# this still has cash and nutri variables until now df5

#%%
"""
Next we will need to separate sust and unsust obs from df5 and make new dfs containing them
> then run the below code once on df5_sust and again on df_unsust

The next few columns we need to run to create a df6 that we will merge with the export_probability data in Monfreda_export.py code
output file = df6_SPAM2010_Feb1324_sust_unsust.xlsx
"""

df5_sust = df5[df5['aei_sust'] == 0]
df5_unsust = df5[df5['aei_sust'] == 1]

#%%     # (1) df5_sust
# CELL 9
# these have 41 frac HA crops and country column
# no cash or nutri vars here
df5_sust = df5_sust[['country']+crops_f2010]

# WIDE TO LONG
# Melt the DataFrame from wide to long format
df6_sust = pd.melt(df5_sust, id_vars=['country'], var_name='crop_year', value_name='HA_frac2010')
# Extract 'crop' and 'year' from 'crop_year'
df6_sust[['crop', 'year']] = df6_sust['crop_year'].str.extract(r'(\D+)(\d+)')
# Drop the 'crop_year' column
df6_sust.drop(columns=['crop_year', 'year'], inplace=True)

# add new column aei_sust=0 for all rows which wil be helpful when we combine df6_sust and df6_unsust
df6_sust['aei_sust'] = 0

# sort by country, crop
df6_sust = df6_sust.sort_values(by=['country','crop'])
# order them
df6_sust = df6_sust[['country', 'crop','aei_sust' ,'HA_frac2010']]

# check country names in df6
df6_sust['country'].unique()

#%% # CELL 10
    # (2) df5_unsust
# Doing the same for unsustainable observations
df5_unsust = df5_unsust[['country']+crops_f2010]

# WIDE TO LONG
# Melt the DataFrame from wide to long format
df6_unsust = pd.melt(df5_unsust, id_vars=['country'], var_name='crop_year', value_name='HA_frac2010')
# Extract 'crop' and 'year' from 'crop_year'
df6_unsust[['crop', 'year']] = df6_unsust['crop_year'].str.extract(r'(\D+)(\d+)')
# Drop the 'crop_year' column
df6_unsust.drop(columns=['crop_year', 'year'], inplace=True)

# add new column aei_sust=1 for all rows which wil be helpful when we combine df6_sust and df6_unsust
df6_unsust['aei_sust'] = 1
# sort by country, crop
df6_unsust = df6_unsust.sort_values(by=['country','crop'])
# order them
df6_unsust = df6_unsust[['country', 'crop','aei_sust' ,'HA_frac2010']]
# check country names in df6
df6_unsust['country'].unique()

## Append df_sust and df_unsust
df6 = pd.concat([df6_sust, df6_unsust], ignore_index=True)
# Export the DataFrame to an Excel file
#df6.to_excel(path+'df6_SPAM2010_Feb1324_sust_unsust.xlsx', index=False) 

#%%
'''
Now making the crop groups at the sustainability level
> calc the % of crop groups at each sustainability level
> export as excel

'''
#%% # CELL 11

# Average the harvested areas at the sustainability level
# Grouping data by aei_sust and averaging up the harvested areas
df7 = df5[['aei_sust'] + frac_columns1]
df7 = df7.groupby(['aei_sust']).mean().reset_index()

# Export the DataFrame to an Excel file
#df7.to_excel(path+'df7_SPAM2010_sust_unsust_feb2024.xlsx', index=False) 
# sum is equal to 1 for all crops for each row [feb13,24]
# this also has cash nutri columns so be careful

#%% CELL 12
# CREATE CROP GROUP VARS BY ADDING FRACTIONAL HA FOR EACH CROP IN THAT GROUP
# 8 crop groups

cereal = ['barl', 'maiz', 'ocer', 'pmil', 'rice', 'smil', 'sorg', 'whea']
fiber = ['cott']
fruitveg = ['bana', 'plnt', 'temf', 'trof', 'vege']
oil = ['cnut', 'oilp', 'ooil', 'rape', 'sesa', 'soyb', 'sunf']
other = ['coco', 'rcof', 'teas']
pulse = ['bean', 'grou', 'opul']
root = ['cass', 'orts', 'pota', 'swpo', 'yams']
sugar = [ 'sugc']

# check if we have 41 crops total
all_crops = cereal+ fiber+ fruitveg + oil +other +pulse +root +sugar
len(all_crops)

# Make new lists adding '2010_f' in each element
cereal_2010 = [crop + '2010_f' for crop in cereal]
fiber_2010 = [crop + '2010_f' for crop in fiber]
fruitveg_2010 = [crop + '2010_f' for crop in fruitveg]
oil_2010 = [crop + '2010_f' for crop in oil]
other_2010 = [crop + '2010_f' for crop in other]
pulse_2010 = [crop + '2010_f' for crop in pulse]
root_2010 = [crop + '2010_f' for crop in root]
sugar_2010 = [crop + '2010_f' for crop in sugar]

# Concatenate all lists and calculate the total length
total_length_2010 = len(cereal_2010 + fiber_2010 + fruitveg_2010 + oil_2010 + other_2010 + pulse_2010 + root_2010 + sugar_2010)
print(str(total_length_2010))

# Step 1: Calculate new columns as the sum for each crop group and year
df7['cereal_2010'] = df7[cereal_2010].sum(axis=1)
df7['fruitveg_2010'] = df7[fruitveg_2010].sum(axis=1)
df7['fiber_2010'] = df7[fiber_2010].sum(axis=1)
df7['oil_2010'] = df7[oil_2010].sum(axis=1)
df7['other_2010'] = df7[other_2010].sum(axis=1)
df7['pulse_2010'] = df7[pulse_2010].sum(axis=1)
df7['root_2010'] = df7[root_2010].sum(axis=1)
df7['sugar_2010'] = df7[sugar_2010].sum(axis=1)


#%% CELL 13
# Step 2: Convert the fractions to percentages by multiplying by 100
crop_type_cols = ['cereal_2010', 'fruitveg_2010', 'fiber_2010', 'oil_2010', 'other_2010', 'pulse_2010', 'root_2010','sugar_2010']

for col in crop_type_cols:
    df7[col] *= 100

# Step 3: Selecting only the required columns to create a new dataframe
df8 = df7[['aei_sust']+crop_type_cols]

# Check if the sum of all crop groups = 100 for 2010
#df8.to_excel(path+'df8.xlsx', index=False)
# looks good feb13,24

#%% CELL 14
#Converting df8 from wide to long format using melt function
df8_long = pd.melt(df8, id_vars=['aei_sust'], var_name='crop_year', value_name='value')

# Generating 'crop' and 'year' columns from 'crop_year' column
df8_long['crop'] = df8_long['crop_year'].apply(lambda x: x.split('_')[0])
df8_long['year'] = df8_long['crop_year'].apply(lambda x: x.split('_')[1])

# Rearranging columns
df8_long = df8_long[['aei_sust', 'year', 'crop', 'value']]

#Export as csv
#df8_long.to_csv(path+'df8_long_by_sustainability.csv', index=False)

#%%
'''
DOING the same for Cash Nutri Data
> taking average at the sustainability level
> and converting from wide to long format

'''
#%% CELL 15
# Moving cash2010_f, nutri2010_f columns to a new df (df5_cash_nutri)
#  select country, aei_sust and the last two columns of df5
df5_cash_nutri = df5[['country', 'aei_sust']].join(df5.iloc[:, -2:])

# Average the harvested areas at the sustainability level
df5_cash_nutri1 = df5_cash_nutri[['aei_sust'] + df4_cash_nutri_frac_columns]
df7_cash_nutri = df5_cash_nutri1.groupby('aei_sust').mean().reset_index()

# Convert the fractions to percentages by multiplying by 100
crop_type_cols = ['cash2010_f', 'nutri2010_f']
for col in crop_type_cols:
    df7_cash_nutri[col] *= 100

# Rename the columns to add an underscore
df7_cash_nutri.rename(columns={'cash2010_f': 'cash_2010', 'nutri2010_f': 'nutri_2010'}, inplace=True)

#Converting df8_cash_nutri from wide to long format using melt function
df8_cash_nutri_long = pd.melt(df7_cash_nutri, id_vars=['aei_sust'], var_name='crop_year', value_name='value')

# Generating 'crop' and 'year' columns from 'crop_year' column
df8_cash_nutri_long['crop'] = df8_cash_nutri_long['crop_year'].apply(lambda x: x.split('_')[0])
df8_cash_nutri_long['year'] = df8_cash_nutri_long['crop_year'].apply(lambda x: x.split('_')[1])

# Rearranging columns
df8_cash_nutri_long = df8_cash_nutri_long[['aei_sust', 'year', 'crop', 'value']]

#Export as csv
#df8_cash_nutri_long.to_csv(path+'df8_cash_nutri_long_by_sustainability.csv', index=False)

#%%
'''
CALCULATE SHANNON DIVERSITY INDEX FOR CROP GROUPS (df8)

'''
#%%  CELL 16
# df8 has % of crop groups, but we need proportions, so we will divide each column by 100

# Create a new df copying df8
df9 = df8.copy()

# (1) Calculate proportions
# It's done by dividing each crop group by tot_HA, we have already done that. RN the data is in % so divide it by 100 to get proportions.

# List of column names to divide by 100
columns_to_divide = ['cereal_2010', 'fruitveg_2010', 'fiber_2010', 'oil_2010', 'other_2010', 'pulse_2010', 'root_2010','sugar_2010']

# Divide each column by 100
df9[columns_to_divide] = df9[columns_to_divide]/100
    
# (2) Generate natural log of proportions
df9['cereal_2010_ln'] = np.log(df9['cereal_2010'])
df9['fruitveg_2010_ln'] = np.log(df9['fruitveg_2010'])
df9['fiber_2010_ln'] = np.log(df9['fiber_2010'])
df9['oil_2010_ln'] = np.log(df9['oil_2010'])
df9['other_2010_ln'] = np.log(df9['other_2010'])
df9['pulse_2010_ln'] = np.log(df9['pulse_2010'])
df9['root_2010_ln'] = np.log(df9['root_2010'])
df9['sugar_2010_ln'] = np.log(df9['sugar_2010'])

# (3) Multiply the Proportions by the Natural Log of the Proportions
df9['cereal_2010_pln'] = df9['cereal_2010'] * df9['cereal_2010_ln']
df9['fruitveg_2010_pln'] = df9['fruitveg_2010'] * df9['fruitveg_2010_ln']
df9['fiber_2010_pln'] = df9['fiber_2010'] * df9['fiber_2010_ln']
df9['oil_2010_pln'] = df9['oil_2010'] * df9['oil_2010_ln']
df9['other_2010_pln'] = df9['other_2010'] * df9['other_2010_ln']
df9['pulse_2010_pln'] = df9['pulse_2010'] * df9['pulse_2010_ln']
df9['root_2010_pln'] = df9['root_2010'] * df9['root_2010_ln']
df9['sugar_2010_pln'] = df9['sugar_2010'] * df9['sugar_2010_ln']

# (4) Calculate the Shannon Diversity Index (sdi)
df9['pln_sum_2010'] = df9[['cereal_2010_pln', 'fruitveg_2010_pln', 'oil_2010_pln', 'other_2010_pln', 'pulse_2010_pln', 'root_2010_pln', 'fiber_2010_pln', 'sugar_2010_pln']].sum(axis=1)
df9['sdi_2010'] = -1 * df9['pln_sum_2010']
df9['sdi_2010'] = df9['sdi_2010'].round(2) # Round the SDI to two decimal places

# Keep only the columns region, sdi_2010 
df9_sdi = df9[['aei_sust','sdi_2010']]

# WIDE TO LONG
df9_sdi_long = pd.melt(df9_sdi, id_vars='aei_sust', var_name='year', value_name='sdi')
# Remove the "sdi_" prefix from the "year" column
df9_sdi_long['year'] = df9_sdi_long['year'].str.replace('sdi_', '')

# Export to csv
#df9_sdi_long.to_csv(path+'df9_sdi_long_by_sustainability.csv', index=False)

#%%

#%%

#%%
''' 
PART II
Now We have to do the same analysis by Region (and sustainability)
> so we will begin from df5 where the data is at country level
> take the average and get the data at regional level, keeping aii_sust var
> then calculate estimates

'''

#%%

#START FROM DF5, COLLAPSE IT AT THE REGIONAL LEVEL
#  it has aei_sust var in it, and we still need it for this part II

# keep the country var and all fractional HA vars for 17 countries
df5_1 = df5[['country', 'aei_sust'] + frac_columns1 ]
# collapse it at country level and aei_sust var
df5_1 = df5_1.groupby(['country', 'aei_sust']).mean().reset_index()
# df5 had 34obs, now df5_1 has 17 - one row per country
# This also has cash nutri fractional vars

# these have 41 frac HA crops and the country column
df5_2010 = df5_1[['country', 'aei_sust']+crops_f2010]

#%%
# WIDE TO LONG
# Melt the DataFrame from wide to long format
# (1) 2010
df6_2010 = pd.melt(df5_2010, id_vars=['country','aei_sust'], var_name='crop_year', value_name='HA_frac2010')
# Extract 'crop' and 'year' from 'crop_year'
df6_2010[['crop', 'year']] = df6_2010['crop_year'].str.extract(r'(\D+)(\d+)')
# Drop the 'crop_year' column
df6_2010.drop(columns=['crop_year'], inplace=True)

# sort by country, crop
df6_1 = df6_2010.sort_values(by=['country','crop'])
# order them
df6_1 = df6_1[['country', 'crop', 'HA_frac2010']]

# Export the DataFrame to an Excel file
#df6_1.to_excel(path+'df6_SPAM2010_regional.xlsx', index=False) 

# No need to export this as it is the same as df6
# Don't think we need this (feb14,23)

# check country names in df6
df6_1['country'].unique()

#%%
'''
Now make the crop groups at the regional level
> calc the % of crop groups at each regional level
> export as excel

'''
#%% # CELL 11

# Average the harvested areas at the sustainability level
# Grouping data by aei_sust and averaging up the harvested areas

# df5 has country , region, and aei_sust vars, but we only need region and aei_sust vars now
df7_1 = df5[['region', 'aei_sust' ] + crops_f2010]
# average at regional level
df7_1 = df7_1.groupby(['region','aei_sust']).mean().reset_index()

# Export the DataFrame to an Excel file
#df7_1.to_excel(path+'df7_1_SPAM2010_feb2024_regional.xlsx', index=False) 
# sum is equal to 1 for all crops for each row [feb14,24]

#%%
# CREATE CROP GROUP VARS BY ADDING FRACTIONAL HA FOR EACH CROP IN THAT GROUP
# 8 crop groups
# we already have the cropgroup lists containing each crop for that group from above, so not repeating that code here again
# cereal, fruitveg, fiber, oil, other, pulse, root, sugar
# We also have the cereal_2010, fruitveg_2010, and so on lists, so not writing again [crop groups for year 2010]

# Step 1: Calculate new columns as the sum for each crop group and year
df7_1['cereal_2010'] = df7_1[cereal_2010].sum(axis=1)
df7_1['fruitveg_2010'] = df7_1[fruitveg_2010].sum(axis=1)
df7_1['fiber_2010'] = df7_1[fiber_2010].sum(axis=1)
df7_1['oil_2010'] = df7_1[oil_2010].sum(axis=1)
df7_1['other_2010'] = df7_1[other_2010].sum(axis=1)
df7_1['pulse_2010'] = df7_1[pulse_2010].sum(axis=1)
df7_1['root_2010'] = df7_1[root_2010].sum(axis=1)
df7_1['sugar_2010'] = df7_1[sugar_2010].sum(axis=1)

# Step 2: Convert the fractions to percentages by multiplying by 100
crop_type_cols = ['cereal_2010', 'fruitveg_2010', 'fiber_2010',  'oil_2010', 'other_2010', 'pulse_2010', 'root_2010','sugar_2010']

for col in crop_type_cols:
    df7_1[col] *= 100

# Step 3: Selecting only the required columns to create a new dataframe
df8_1 = df7_1[['region','aei_sust']+crop_type_cols]

#df8_1.to_excel(path+'df8_1.xlsx', index=False)
# Checked the sum of all crop groups = 100 for 2010 [feb14,24]
#%%
# We also need the crop mixes for Global (all data) for sust and unsust
# So I'll take an average over df8_1 over aei_sust var

# keep aei_sust and crop type columns
df8_2 = df8_1[['aei_sust' ] + crop_type_cols]
# average at regional level
df8_2 = df8_2.groupby(['aei_sust']).mean().reset_index()
df8_2['region'] = 'Overall' # add a column region

# Append this df8_2 with df8_1  
df8_1 = pd.concat([df8_1, df8_2], ignore_index=True)

#Converting df8_1 from wide to long format using melt function
df8_1_long = pd.melt(df8_1, id_vars=['region','aei_sust'], var_name='crop_year', value_name='value')

# Generating 'crop' and 'year' columns from 'crop_year' column
df8_1_long['crop'] = df8_1_long['crop_year'].apply(lambda x: x.split('_')[0])
df8_1_long['year'] = df8_1_long['crop_year'].apply(lambda x: x.split('_')[1])

# Rearranging columns
df8_1_long = df8_1_long[['region','aei_sust', 'year', 'crop', 'value']]

#Export as csv
df8_1_long.to_csv(path+'df8_1_long_by_region.csv', index=False)

# This df has the regional as well as the overall croptype HA % for sust and unsust levels


#%%


#%% CELL 
# DOING THE SAME FOR CASH NUTRI DATA
# GETTING THE REGIONAL AND SUST AVERAGES 

# Moving cash2010_f, nutri2010_f columns to a new df (df5_cash_nutri)
#  select country, aei_sust and the last two columns of df5
df5_cash_nutri_1 = df5[['region', 'aei_sust']].join(df5.iloc[:, -2:])

# Average the harvested areas at the sustainability level
df5_cash_nutri_2 = df5_cash_nutri_1[['region','aei_sust'] + df4_cash_nutri_frac_columns]
df7_cash_nutri_1 = df5_cash_nutri_2.groupby(['region', 'aei_sust']).mean().reset_index()
# this df has cash and nutri fractions at regional and sust level

# Convert the fractions to percentages by multiplying by 100
crop_type_cols = ['cash2010_f', 'nutri2010_f']
for col in crop_type_cols:
    df7_cash_nutri_1[col] *= 100

# Rename the columns to add an underscore
df7_cash_nutri_1.rename(columns={'cash2010_f': 'cash_2010', 'nutri2010_f': 'nutri_2010'}, inplace=True)

#Converting df8_cash_nutri from wide to long format using melt function
df8_cash_nutri_1_long = pd.melt(df7_cash_nutri_1, id_vars=['region','aei_sust'], var_name='crop_year', value_name='value')

# Generating 'crop' and 'year' columns from 'crop_year' column
df8_cash_nutri_1_long['crop'] = df8_cash_nutri_1_long['crop_year'].apply(lambda x: x.split('_')[0])
df8_cash_nutri_1_long['year'] = df8_cash_nutri_1_long['crop_year'].apply(lambda x: x.split('_')[1])

# Rearranging columns
df8_cash_nutri_1_long = df8_cash_nutri_1_long[['region', 'aei_sust', 'year', 'crop', 'value']]

# We will add region var to df8_cash_nutri_long
df8_cash_nutri_long['region'] = 'Overall' # add a column region

# Append this df8_2 with df8_1  
df8_cash_nutri_1_long = pd.concat([df8_cash_nutri_1_long, df8_cash_nutri_long], ignore_index=True)

#Export as csv
df8_cash_nutri_1_long.to_csv(path+'df8_cash_nutri_1_long_by_sust.csv', index=False)


#%%
'''
CALCULATE SHANNON DIVERSITY INDEX FOR CROP GROUPS (df8)

'''
#%%  CELL 16
# df8 has % of crop groups, but we need proportions, so we will divide each column by 100

# Create a new df copying df8
df9_1 = df8_1.copy()

# (1) Calculate proportions
# It's done by dividing each crop group by tot_HA, we have already done that. RN the data is in % so divide it by 100 to get proportions.

# List of column names to divide by 100
columns_to_divide = ['cereal_2010', 'fruitveg_2010', 'fiber_2010', 'oil_2010', 'other_2010', 'pulse_2010', 'root_2010','sugar_2010']

# Divide each column by 100
df9_1[columns_to_divide] = df9_1[columns_to_divide]/100
    
# (2) Generate natural log of proportions
df9_1['cereal_2010_ln'] = np.log(df9_1['cereal_2010'])
df9_1['fruitveg_2010_ln'] = np.log(df9_1['fruitveg_2010'])
df9_1['fiber_2010_ln'] = np.log(df9_1['fiber_2010'])
df9_1['oil_2010_ln'] = np.log(df9_1['oil_2010'])
df9_1['other_2010_ln'] = np.log(df9_1['other_2010'])
df9_1['pulse_2010_ln'] = np.log(df9_1['pulse_2010'])
df9_1['root_2010_ln'] = np.log(df9_1['root_2010'])
df9_1['sugar_2010_ln'] = np.log(df9_1['sugar_2010'])

# (3) Multiply the Proportions by the Natural Log of the Proportions
df9_1['cereal_2010_pln'] = df9_1['cereal_2010'] * df9_1['cereal_2010_ln']
df9_1['fruitveg_2010_pln'] = df9_1['fruitveg_2010'] * df9_1['fruitveg_2010_ln']
df9_1['fiber_2010_pln'] = df9_1['fiber_2010'] * df9_1['fiber_2010_ln']
df9_1['oil_2010_pln'] = df9_1['oil_2010'] * df9_1['oil_2010_ln']
df9_1['other_2010_pln'] = df9_1['other_2010'] * df9_1['other_2010_ln']
df9_1['pulse_2010_pln'] = df9_1['pulse_2010'] * df9_1['pulse_2010_ln']
df9_1['root_2010_pln'] = df9_1['root_2010'] * df9_1['root_2010_ln']
df9_1['sugar_2010_pln'] = df9_1['sugar_2010'] * df9_1['sugar_2010_ln']

# (4) Calculate the Shannon Diversity Index (sdi)
df9_1['pln_sum_2010'] = df9_1[['cereal_2010_pln', 'fruitveg_2010_pln', 'oil_2010_pln', 'other_2010_pln', 'pulse_2010_pln', 'root_2010_pln', 'fiber_2010_pln', 'sugar_2010_pln']].sum(axis=1)
df9_1['sdi_2010'] = -1 * df9_1['pln_sum_2010']
df9_1['sdi_2010'] = df9_1['sdi_2010'].round(2) # Round the SDI to two decimal places

# Keep only the columns region, sdi_2010 
df9_1_sdi = df9_1[['aei_sust','region', 'sdi_2010']]

# WIDE TO LONG
df9_1_sdi_long = pd.melt(df9_1_sdi, id_vars=['aei_sust','region'], var_name='year', value_name='sdi')
# Remove the "sdi_" prefix from the "year" column
df9_1_sdi_long['year'] = df9_1_sdi_long['year'].str.replace('sdi_', '')

# Export to csv
df9_1_sdi_long.to_csv(path+'df9_1_sdi_long_by_sustainability.csv', index=False)
#%%


























