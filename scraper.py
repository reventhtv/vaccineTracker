from bs4 import BeautifulSoup
import requests, time
from bs4 import BeautifulSoup as soup
from time import sleep, strftime
from random import randint
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
from urllib.request import urlopen as uReq
import requests
import csv
import json
import matplotlib.pyplot as plt
import seaborn as sns

'''
Åldersgrupp       : Agegroup
Antal vaccinerade : Number of vaccinated
Andel vaccinerade : Proportion of vaccinated
Dosnummer         : Dosenumber
'''

xls = pd.ExcelFile("https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data")

xls1 = pd.read_excel(xls, 'Vaccinerade ålder')

#print(xls1.columns)

# Let's drop unnamed column from the dataframe
df = xls1.drop("Unnamed: 5", axis=1)
#print(df.columns)

#Now we will seperate dose1 and dose2 of entire sweden
df_sweden_dose1 = df.loc[0:8]
print(df_sweden_dose1)

df_sweden_dose2 = df.loc[9:17]
#print(df_sweden_dose2)




df1 = df.loc[18:] #Region wise dataframe with both Dos 1 and Dos 2
#print(df1.head())

#We will seperate a region "Stockholm" from "Region" column
df1_region = pd.DataFrame(df1)
df1_region.set_index("Region", inplace=True)
#.loc["Stockholm"] this will help to fetch value Stockholm from column Region
#print(df1_region)

#We will seperate dos1 and dos2 "Region" wise

df1_region_dos1 = df1_region.loc[df1_region['Dosnummer'] == 'Dos 1']
#print(df1_region_dos1)

#data.loc[data['first_name'] == 'Antonio', 'city':'email']

df1_region_dos2 = df1_region.loc[df1_region['Dosnummer'] == 'Dos 2']
#print(df1_region_dos2)


#Now let's fetch Dos1 of region Stockholm

df1_region_stockolm_dos1 = df1_region_dos1.loc["Stockholm"]
#print(df1_region_stockolm_dos1)

df1_region_skåne_dos1 = df1_region_dos1.loc["Skåne"]
print(df1_region_skåne_dos1)

df1_region_västra_götaland_dos1 = df1_region_dos1.loc["Västra Götaland"]
print(df1_region_västra_götaland_dos1)

df_sweden_dose1.set_index("Region", inplace=True)
print(df_sweden_dose1)



# Create a data correlation dataframe:

#Make a list of columns to drop
df_sweden_dose1 = df_sweden_dose1.drop(columns=["Dosnummer", "Andel vaccinerade"])
#print(df_sweden_dose1)
df1_region_stockolm_dos1 = df1_region_stockolm_dos1.drop(columns=["Dosnummer", "Andel vaccinerade"])
#print(df1_region_stockolm_dos1)
df1_region_skåne_dos1 = df1_region_skåne_dos1.drop(columns=["Dosnummer", "Andel vaccinerade"])
print(df1_region_skåne_dos1)
df1_region_västra_götaland_dos1 = df1_region_västra_götaland_dos1.drop(columns=["Dosnummer", "Andel vaccinerade"])
print(df1_region_västra_götaland_dos1)
#corr_df_master = pd.DataFrame()


#Reset index to merge dataframes
df_sweden_dose1.reset_index(inplace=True)
#print(df_sweden_dose1)
df1_region_stockolm_dos1.reset_index(inplace=True)
#print(df1_region_stockolm_dos1)
df1_region_skåne_dos1.reset_index(inplace=True)
print(df1_region_skåne_dos1)
df1_region_västra_götaland_dos1.reset_index(inplace=True)
print(df1_region_västra_götaland_dos1)
df_merge = df_sweden_dose1.merge(df1_region_stockolm_dos1, how='outer')
#print(df_merge)
df_merge_skåne = df_merge.merge(df1_region_skåne_dos1, how='outer')
print(df_merge_skåne)
df_merge_västra_götaland = df_merge_skåne.merge(df1_region_västra_götaland_dos1, how='outer')
print(df_merge_västra_götaland)
#Now we will re-arrange our data using pivot tables for better processing
arrangedData = df_merge_västra_götaland.pivot_table('Antal vaccinerade', ['Åldersgrupp'], 'Region')
print(arrangedData)
print(arrangedData.columns) #Index(['Stockholm', '| Sverige |'], dtype='object', name='Region')


print(arrangedData.describe())



# Create a data correlation dataframe:
corr_df_master = arrangedData.corr()
corr_target = corr_df_master.iloc[3][:] # The correlation target is the 'Sverige' column
corr = corr_target.sort_values(ascending=True)
corr_df = pd.DataFrame(corr)
corr_df.reset_index(level=0, inplace=True)
corr_df.columns = ['Regions', 'correlation']
print(corr_df)

sns.relplot(x='Regions', y='correlation', data=corr_df, aspect=3)
plt.ylim([0.85, 1.05])
plt.xticks(rotation=60)

# Correlation reference line at y=0
f = len(corr_df.Regions) -1
plt.plot([0, f], [0, 0], linewidth=1, c='orange')
#plt.show()

# Observing the distribution of correlation coeficients
fig, ax = plt.subplots(figsize=(24, 12))
sns.distplot(corr_df.correlation, kde=True, bins = 10, ax=ax)

plt.xlim([0.88, 1.08])
plt.ylabel('Number of Regions')
plt.xlabel('Correlation 0.8 to 1.08')
ax.set_title("Distribution of correlation coefficients\n");

# Correlation reference line at x=1
plt.plot([1, 1], [0, 4], linewidth=1, c='orange', linestyle='--');
#plt.show()

age1=df1_region_västra_götaland_dos1['Antal vaccinerade']
sns.distplot(age1,kde=True)
#plt.show()


Total_sweden_dos1 = df_sweden_dose1['Antal vaccinerade'].loc[8]
print(Total_sweden_dos1)

#Calculate mean across all age groups in sweden
Total_sweden_dos1_mean = df_sweden_dose1['Antal vaccinerade'].loc[0:7].mean()
print(Total_sweden_dos1_mean)


xls2 = xls1 = pd.read_excel(xls, 'Vaccinerade kommun')

#print(xls2.head())

#let's drop "unnamed" columns

df_kommun = xls2.drop(["Andel_dos1","Andel_dos2","Unnamed: 6", "Unnamed: 7", "Unnamed: 8"], axis=1)
print(df_kommun.head())



#Let's seperate specific cities from the dataframe to another dataframe
df_kommun_malmö = df_kommun[df_kommun["KnNamn"]=='Malmö']
print(df_kommun_malmö)

df_kommun_stockholm = df_kommun[df_kommun["KnNamn"]=='Stockholm']
print(df_kommun_stockholm)

df_kommun_goteborg = df_kommun[df_kommun["KnNamn"]=='Göteborg']
print(df_kommun_goteborg)


print("Total number of dos1 delivered in sweden %d\n" % df_kommun['Antal_dos1'].sum())
print("Total number of dos2 delivered in sweden %d\n" % df_kommun['Antal_dos2'].sum())

df_merged_kommuns = pd.merge(pd.merge(df_kommun_malmö,df_kommun_goteborg,how='outer'),df_kommun_stockholm,how='outer')
print(df_merged_kommuns)

df_total = df_merged_kommuns(columns=['KnNamn'])




