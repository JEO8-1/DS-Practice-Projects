import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

#imports all csv files from the folder and stores in a list, asuuming this python file is in the same folder as the files
path = os.getcwd() 
csv_files = glob.glob(os.path.join(path, "*.csv")) 
dataframes = []

#creates dataframes for each file and stores them in the dataframes list
for file in csv_files: 
    df = pd.read_csv(file) 
    dataframes.append(df)
    
x = list(range(1,32))    

#lists that contain the values passed from the dataframes
list_of_total_confirmed = []
list_of_total_deaths = []

#Gets the sums for the 'Confirmed' and 'Deaths' Columns
def get_sums (df):
    confirmed = df['Confirmed'].sum()
    deaths = df['Deaths'].sum()
    list_of_total_confirmed.append(confirmed)
    list_of_total_deaths.append(deaths)

#Gets the values on Decemeber 31 to be used for the previous day    
dec31 = pd.read_csv('/Users/owengraham/Data Science/DS-Practice-Projects/Group project MAST4016/Data/12.31 US.csv')
dec31Death = dec31['Deaths'].sum()
dec31Confirmed = dec31['Confirmed'].sum()

#Subtracts a current day by the previous day to find the daily change
def find_dailyvalue(startervalue, alist):
    sorted_values = sorted(alist) #this line is necessary because the data not in chronological order in the dataframe list
    previous = startervalue
    daily_value_list = []
    
    for x in sorted_values:
        daily_value = x - previous
        daily_value_list.append(daily_value)
        previous = x

    return daily_value_list  
    
#Applies the get sums function to every file in the dataframes list
for file in dataframes:
    get_sums(file)
      
#a list of the daily changes in deaths    
daily_deaths  = find_dailyvalue(dec31Death, list_of_total_deaths)

#a list of the daily changes in confirmed cases
daily_Confirmed = find_dailyvalue(dec31Confirmed, list_of_total_confirmed)

plt.xlabel('Day of Month')

plt.plot(x, daily_deaths, label = 'Recorded Data')
plt.ylabel('Number of Deaths')
plt.title('US Daily Covid Deaths, January 2023')

# plt.plot(x, daily_Confirmed, label = 'Recorded Data')
# plt.ylabel('Number of Confirmed Cases')
# plt.title('US Daily Confirmed Covid Cases, January 2023')


#Additional code to be used for the weekly averages

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
plt.plot(weekly, weekly_averages_Deaths, marker = 'o', label  = 'Weekly Average')

weekly_average_confirmed = [cweek1, cweek2, cweek3, cweek4, cweek5]
#plt.plot(weekly, weekly_average_confirmed, marker = 'o', label = 'Weekly Average')

plt.legend()

#Code to compute the daily average over the month
monthly_average_deaths = np.array(daily_deaths).mean()
monthly_average_confirmed = np.array(daily_Confirmed).mean()

print('Us deaths: ', monthly_average_deaths/ 334.2) 
print('Us confirmed: ',monthly_average_confirmed/334.2)

print(weekly_averages_Deaths)

