# -*- coding: utf-8 -*-
"""
Feb15,2024 - Piyush Mehta

Paper2 - FAOSTAT Export probability for SPAM2010 data for sust/unsust at regional level
> for each crop, taking the average of export probability (Export/Production) for years 2010-2015 for SPAM 2010 data
> 

"""
#%%
import os
import pandas as pd
# Set the option to display all columns
pd.set_option('display.max_columns', None)
#original path
path = "D:\\Delaware\\Work\\Paper2_Irrigation_Nutrition\\Data\\Crop_mixes\\MAP_SPAM\\Total_HA_2010\\export_propensity\\"
os.chdir(path)

# Read the Ratio sheet
df_1 = pd.read_excel(path+"SPAM_export.xlsx", sheet_name= "Sheet1")
df_2 = pd.read_excel(path+"SPAM_export.xlsx", sheet_name= "Sheet2")

#%%
# the itemcode for rice and groundnut is different in SHeet2, so replace them with their itemcode in SHeet1, as we will be using the itemcode for SHeet1 for the combined data
# replace all values from F2552 to F2556, and F2807 to F2805 in Sheet2 data (df_2)
df_2['itemcode'] = df_2['itemcode'].replace({'F2552': 'F2556', 'F2807': 'F2805'})

# combine df_1 and df_2 and save as df
df = pd.concat([df_1, df_2], ignore_index=True)
df.drop_duplicates(inplace=True) # drop duplicates
df = df.sort_values(by=["country","Element","itemcode","year"]) # sort data

# List of food item codes to keep
# These are the itemcodes that match with the common crops that we have for both faostat and SPAM2010
# 31 itemcodes (faostat), but they matched with 33 crops in SPAM
itemcodes_to_keep = ['F2513', 'F2514', 'F2520', 'F2517', 'F2805', 'F2517', 'F2518', 'F2511', 'F2559', 'F2615', 'F2616', 'F2625', 'F2625', 'F2605', 'F2560', 'F2562', 'F2586', 'F2558', 'F2561', 'F2555', 'F2557', 'F2633', 'F2630', 'F2635', 'F2546', 'F2556', 'F2549', 'F2532', 'F2534', 'F2531', 'F2533', 'F2535', 'F2536']

# Filter data to keep only the specified food items
df1 = df[df['itemcode'].isin(itemcodes_to_keep)]

# filter based on years 
years_to_keep = [2010, 2011, 2012, 2013, 2014, 2015]
df1 = df1[df1['year'].isin(years_to_keep)]

#%%
# Make a separate dfs for Production quantity and Export quantity
df2 = df1[df1['Element'] == 'Production']

df3 = df1[df1['Element'] == 'Export Quantity']

# Mapping of itemcodes to crop names
# Note - these are only the 31 food items, and not 33 crops 
# for this data, we have 31 unique items, and 33 SPAM2010
# we will combine the spam info for F2517 and F2625
# using the common name millet for F2517, and so on from sheet3 (crop_common column) in SPAM_export.xlsx
# F2517 and F2625 have duplicates for spam2010, but I've written it once here, and used the common name of that crop (F2517:millet, F2625:fruit)

itemcode_to_crop = {'F2511': 'whea', 'F2513': 'barl', 'F2514': 'maiz', 'F2517': 'millet', 'F2518': 'sorg', 'F2520': 'ocer', 'F2531': 'pota', 'F2532': 'cass', 'F2533': 'swpo', 'F2534': 'orts', 'F2535': 'yams', 'F2536': 'sugc', 'F2546': 'bean', 'F2549': 'opul', 'F2555': 'soyb', 'F2556': 'grou', 'F2557': 'sunf', 'F2558': 'rape', 'F2559': 'cott', 'F2560': 'cnut', 'F2561': 'sesa', 'F2562': 'oilp', 'F2586': 'ooil', 'F2605': 'vege', 'F2615': 'bana', 'F2616': 'plnt', 'F2625': 'fruit', 'F2630': 'rcof', 'F2633': 'coco', 'F2635': 'teas', 'F2805': 'rice'}

# Create the 'crop' column using the itemcode_to_crop mapping
df2['crop'] = df2['itemcode'].map(itemcode_to_crop)
df3['crop'] = df3['itemcode'].map(itemcode_to_crop)

df2 = df2.sort_values(by=['country', 'crop', 'year'])
df3 = df3.sort_values(by=['country', 'crop', 'year'])

#%%
# df2 has production quantities, df3 has export quantities
df2.rename(columns={'Value_thousandtonnes': 'production'}, inplace=True)
df3.rename(columns={'Value_thousandtonnes': 'export'}, inplace=True)

# Group the DataFrame by 'country', 'year', and 'crop', and calculate the sum of 'production' and 'export' quanities
df4 = df2.groupby(['country', 'year', 'crop'])['production'].sum().reset_index()
df5 = df3.groupby(['country', 'year', 'crop'])['export'].sum().reset_index()

# Merge df4 and df5 to have production and export quantities together
df6 = df4.merge(df5, on=['crop', 'country', 'year'], how='inner')

# Calc export ratio by dividing export by production
df6['export_ratio'] = df6['export']/df6['production']

#%%
# Drop observations with ratio = nan  and inf
df6 = df6.dropna(subset=['export_ratio'])
df6 = df6[df6['export_ratio'] != float('inf')]
df6 = df6[df6['export_ratio'] != 0] # Drop rows where export_ratio is 0
#df6_filtered = df6[df6['export_ratio'] > 1]

# Set the value of ratio = 1 if it is greater than 1 (as Kyle did for his LSLA file)
df6.loc[df6['export_ratio'] > 1, 'export_ratio'] = 1

df6 = df6.sort_values(by=['country', 'crop', 'year']) # sort

#rename obs with country = United Republic of Tanzania to Tanzania
df6.loc[df6['country'] == 'United Republic of Tanzania', 'country'] = 'Tanzania'

#26 countries
# MAKE SURE THE COUNTRY NAME IS THE SAME AS THESE
countries = ["Angola", "Bangladesh", "Benin", "Cambodia", "Cameroon", "Congo", "Egypt", "Ethiopia", "Ghana", "Guinea", "Haiti", "Jordan", "Kenya", "Lesotho", "Liberia", "Madagascar", "Malawi", "Mali", "Nepal", "Nigeria", "Peru", "Philippines", "Rwanda", "Tanzania", "Uganda", "Zimbabwe"]
df6['country'].unique()  # check country names

# Take average of export_ratio for each crop and country; 
df7 = df6.groupby(['country', 'crop'])['export_ratio'].mean()
df7 = df7.reset_index() # series to dataframe

# This df we have the average of export ratios at crop country level over years 2010-2015
# these ratios will be the same for sust and unsust level before multiplying it with the crop specific HAs

#%%
# adding region variable
df7['region'] = ''
# Specify the columns for which we want to calculate the average
america = ["Haiti", "Peru"]
asia = ["Bangladesh", "Cambodia", "Nepal", "Philippines"]
middle_east = ["Egypt", "Jordan"] # Congo Democratic Republic is Congo
southeast_africa = ["Angola", "Congo", "Ethiopia", "Kenya", "Lesotho", "Madagascar", "Malawi", "Rwanda", "Tanzania", "Uganda", "Zimbabwe"]
west_africa = ["Benin", "Cameroon", "Ghana", "Guinea", "Liberia", "Mali", "Nigeria"]
# Replace 'region' values based on conditions
df7.loc[df7['country'].isin(america), 'region'] = 'America'
df7.loc[df7['country'].isin(asia), 'region'] = 'Asia'
df7.loc[df7['country'].isin(middle_east), 'region'] = 'Middle East'
df7.loc[df7['country'].isin(southeast_africa), 'region'] = 'Southern/East Africa'
df7.loc[df7['country'].isin(west_africa), 'region'] = 'West Africa'

#%%
''' WE DONT NEED THIS [FEB 2024]
 
# We calculated country and regional counts from df3 in Monfreda_weighted_HA.py
# making the same data here as well
# DHS cluster count per sust/unsust per COUNTRY in df3 in DHS/SPAM data
data = {'country': ['Bangladesh', 'Bangladesh', 'Cambodia', 'Cambodia', 'Cameroon', 'Cameroon', 'Egypt', 'Egypt',
'Ethiopia', 'Ethiopia', 'Haiti', 'Haiti', 'Jordan', 'Jordan', 'Kenya', 'Kenya', 'Madagascar', 'Madagascar','Malawi', 'Malawi', 'Mali', 'Mali', 'Nepal', 'Nepal', 'Nigeria', 'Nigeria', 'Peru', 'Peru',
'Philippines', 'Philippines', 'Tanzania', 'Tanzania', 'Zimbabwe', 'Zimbabwe'],
    'aei_sust': [0, 1] * 17,  # Repeating '0' and '1' to match 36 rows
    'count': [91, 887, 177, 635, 28, 9, 35, 1073, 1, 6, 369, 126, 217, 110, 511, 19, 40, 4, 1214, 56, 39, 56, 169, 188, 363, 44, 824, 30, 88, 7, 303, 13, 216, 16]}
country_count = pd.DataFrame(data)
'''
#%% 
# Importing df6 (df6_SPAM2010_Feb1324_sust_unsust.xlsx) data as df8 exported earlier using SPAM2010_HA_sust_unsust_2024Feb.py
# It contains averaged fractional HA for each crop for all countries
df8 = pd.read_excel(r"D:\\Delaware\\Work\\Paper2_Irrigation_Nutrition\\Data\\Crop_mixes\\MAP_SPAM\Total_HA_2010\\df6_SPAM2010_Feb1324_sust_unsust.xlsx", sheet_name= "Sheet1")

# This file has 33 crops, and export data has 31. We need to average the HA for the following crops, to make the HA data for 31 crops as well
# We are doing this because FAOSTAT export data items are combined for a few crops for which we have individual data from SPAM
# Crops to take mean over - 
# (1) Millets and products item is equivalent to the 2 crops in spam2010 = [pmil, smil]
# (2) Fruits,other = 2 crops = [temf,trof]

# Extract the data for these crops, take average, then append it to df8 again
# create separate df for each crop category below
# 4 crops in total
millet = ['pmil', 'smil']
fruit = ['temf', 'trof']

# Create a subset of df8 with only the selected crops (case-insensitive)
df8_millet = df8[df8['crop'].str.lower().isin(map(str.lower, millet))]
df8_fruit = df8[df8['crop'].str.lower().isin(map(str.lower, fruit))]

# Take average
df8_millet_1 = df8_millet.groupby(['country','aei_sust'])[['HA_frac2010']].mean().reset_index()
df8_fruit_1 = df8_fruit.groupby(['country','aei_sust'])[['HA_frac2010']].mean().reset_index()

# Note - Using the same names for these crops as we used in itemscode_to_crop (from Sheet3 in SPAM_export.xlsx)

# Add a new 'crop' column with the value 'millet'
df8_millet_1['crop'] = 'millet'
df8_fruit_1['crop'] = 'fruit'

# From df8, remove the crops that we just took an average over 
# Create a condition to filter rows where 'crop' is not in the specified lists
condition = ~df8['crop'].isin(millet + fruit )

# Apply the condition to the DataFrame to filter the rows
# removed 4 crops, so we are left with 31 per country
df8_removed = df8[condition]
df8_removed.reset_index(drop=True, inplace=True)

# Append the dfs with averaged values and df8_removed, and save as df8_updated
# Now we have 50 items per country - (same as Sheet3_unique)
df8_updated = pd.concat([df8_millet_1, df8_fruit_1, df8_removed], ignore_index=True)
df8_updated = df8_updated.sort_values(by=['aei_sust','country', 'crop']) # sort
df8_updated = df8_updated[['aei_sust','country', 'crop','HA_frac2010']] #order
df8_updated = df8_updated.reset_index(drop=True)

#%%
# merge df7 (export ratios) and df8 (SPAM2010 fractional HA) based on country and crop columns
df9 = pd.merge(df7, df8_updated, on=['country', 'crop'], how='inner')
#ordering vars
df9 = df9[['region','country','crop','aei_sust','export_ratio', 'HA_frac2010']]

#sample size
df9_counts = df9.groupby(['aei_sust','region']).size().reset_index(name='count')
#  observations each


#%%
# Here we use the fractional HA for each crop as the weight
# multiply the 'export_ratio' values by the corresponding 'HA_frac2010' values for each country and sum them up
# group the DataFrame by 'country' and calculates the sum of 'HA_frac2000' values for each country for the year 2010.
# then divide the 'weighted_sum_export_r2000' by 'sum_HA_frac2000' to compute the weighted average export ratio for the year 2010 for each country.

# (1) Calculate the weighted sum of export ratios for each country for the year 2010
weighted_sum_export_r2010 = df9.groupby(['aei_sust','country'])['export_ratio'].apply(lambda x: (x * df9['HA_frac2010']).sum())
# Calculate the sum of HA_frac2010 for each country for the year 2010
sum_HA_frac2010 = df9.groupby(['aei_sust','country'])['HA_frac2010'].sum()
# Calculate the weighted average export ratio for the year 2010
weighted_avg_export_r2010 = weighted_sum_export_r2010 / sum_HA_frac2010
# Create a new DataFrame to store the results
df10 = weighted_avg_export_r2010.reset_index()
# rename column to ratio2010
df10 = df10.rename(columns={df10.columns[2]: 'weighted_avg_export_r2010'})


#%%
# adding region variable (using half code from above)
df10['region'] = ''
# Replace 'region' values based on conditions
df10.loc[df10['country'].isin(america), 'region'] = 'America'
df10.loc[df10['country'].isin(asia), 'region'] = 'Asia'
df10.loc[df10['country'].isin(middle_east), 'region'] = 'Middle East'
df10.loc[df10['country'].isin(southeast_africa), 'region'] = 'Southern/East Africa'
df10.loc[df10['country'].isin(west_africa), 'region'] = 'West Africa'

# order vars
df10 = df10[['aei_sust','region','country','weighted_avg_export_r2010']]

# Export the DataFrame to an Excel file
#df10.to_excel(path+'df10.xlsx', index=False) 

#%%

# Take average over aei_sust and region variable 
df11 = df10.groupby(['aei_sust','region'])[['weighted_avg_export_r2010']].mean().reset_index()

# We also need the overall export ratios to include in the figure, so I will collape the data and take the means over aei_sust
df11_overall = df10.groupby(['aei_sust'])[['weighted_avg_export_r2010']].mean().reset_index()
# Add a new column 'region' with value 'Overall'
df11_overall['region'] = 'Overall'

df12 = pd.concat([df11, df11_overall], ignore_index=True)

# Rename the 'final_weighted_export_r2000' column to '2000' and 2020 resp
df12.rename(columns={'weighted_avg_export_r2010': 'export_propensity'}, inplace=True)

#export to excel
df12.to_excel(path+'Export_propensity_sust_unsust_SPAM2010.xlsx', index=False) 

#%%
''' USED R TO MAKE THE FIGURE [feb16,24]
import matplotlib.pyplot as plt
# Assuming you have your data loaded in df12
regions = df12['region']
values_2000 = df12['final_weighted_export_r2000']
values_2020 = df12['final_weighted_export_r2020']

plt.figure(figsize=(10, 6))
plt.scatter(values_2000, regions, label='2000', alpha=0.5, color='blue', marker='o')
plt.scatter(values_2020, regions, label='2020', alpha=0.5, color='red', marker='s')

plt.title('Scatter Plot of Export Ratios by Region (2000 vs. 2020)')
plt.xlabel('Final Weighted Export Ratio')
plt.ylabel('Region')

plt.legend(loc='best')
plt.grid(True)
plt.tight_layout()

# Save the plot with DPI=600
plt.savefig(path+'Export_probability1.png', dpi=600)
plt.show()
'''
#%%

