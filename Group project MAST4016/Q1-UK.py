import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

#Only works if this file is in the same directory as all the other files
path = os.getcwd() 
csv_files = glob.glob(os.path.join(path, "*.csv")) 
dataframes = []

x = list(range(1,32))   

for file in csv_files: 
    df = pd.read_csv(file) 
    dataframes.append(df)
    
jan1 = pd.read_csv('01-01-2023.csv')

list_of_total_confirmed = []
list_of_total_deaths = []
correct_areas = ['Wales', 'England', 'Northern Ireland', 'Scotland']

def filter_to_Main_UK (df):
    mainUK = df['Province_State'].isin(correct_areas)
    df_mainUk = df[mainUK]
    confirmed = df_mainUk['Confirmed'].sum()
    deaths = df_mainUk['Deaths'].sum()
    #print(df_mainUk.reindex(columns = ['Last_Update','Confirmed', 'Deaths', 'Combined_Key']))
    list_of_total_confirmed.append(confirmed)
    list_of_total_deaths.append(deaths)


#Gets the value on Decemeber 31 to be used for the previous day     
dec31 = pd.read_csv('/Users/owengraham/Data Science/DS-Practice-Projects/Group project MAST4016/Data/12-31-2022.csv')
mainland = dec31['Province_State'].isin(correct_areas)
df_mainland = dec31[mainland]

#The values to be used in the find_daily_value function
dec31_Deaths = df_mainland['Deaths'].sum()
dec31_Confirmed = df_mainland['Confirmed'].sum()

def find_dailyvalue(startervalue, alist):
    sorted_values = sorted(alist) #this line is necessary because the data is out of place in the list
    previous = startervalue
    daily_value_list = []
    
    for x in sorted_values:
        daily_value = x - previous
        daily_value_list.append(daily_value)
        previous = x

    return daily_value_list


#Processes all the files in the folder 
for file in dataframes:
    filter_to_Main_UK(file)
        
daily_deaths = find_dailyvalue(dec31_Deaths, list_of_total_deaths)
daily_Confirmed = find_dailyvalue(dec31_Confirmed, list_of_total_confirmed)

plt.xlabel("Day of Month")


# plt.plot(x, daily_deaths, label = 'Recorded Data')
# plt.ylabel('Number of Deaths')
# plt.title('UK Daily Covid Deaths, January 2023')

plt.plot(x, daily_Confirmed, label = 'Recorded Data')
plt.ylabel('Number of Confirmed Cases')
plt.title('UK Daily Confirmed Covid Cases, January 2023')

#Data and code to be used for the weekly averages
weekly = [7,14,21,28,31]

dweek1 = np.array(daily_deaths[0:7]).mean()
dweek2 = np.array(daily_deaths[7:14]).mean()
dweek3 = np.array(daily_deaths[14:21]).mean()
dweek4 = np.array(daily_deaths[21:28]).mean()
dweek5 = np.array(daily_deaths[28:]).mean()

cweek1 = np.array(daily_Confirmed[0:7]).mean()
cweek2 = np.array(daily_Confirmed[7:14]).mean()
cweek3 = np.array(daily_Confirmed[14:21]).mean()
cweek4 = np.array(daily_Confirmed[21:28]).mean()
cweek5 = np.array(daily_Confirmed[28:]).mean()

weekly_averages_Deaths = [dweek1, dweek2, dweek3, dweek4, dweek5]
weekly_average_confirmed = [cweek1, cweek2, cweek3, cweek4, cweek5]

#plt.plot(weekly, weekly_averages_Deaths, marker = 'o', label = 'Weekly Average')
plt.plot(weekly, weekly_average_confirmed, marker = 'o', label = 'Weekly Average')

plt.legend()

#Code to compute the daily average over the month
monthly_average_deaths = np.array(daily_deaths).mean()
monthly_average_confirmed = np.array(daily_Confirmed).mean()

print(monthly_average_deaths / 67.7)
print(monthly_average_confirmed / 67.7)