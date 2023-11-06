
# Uncomment the pip install code below if you haven't installed these libraries yet
#!pip install pandas
#!pip install zipfile
#!pip install kaggle

# import the pandas library
import pandas as pd

# import zipfile library (we will use this to extract the file downloaded from Kaggle)
import zipfile

# import kaggle library (we will use this to download the dataset programatically from Kaggle)
import kaggle

# download dataset from kaggle using the Kaggle API
# !kaggle datasets download -d hmavrodiev/movies_rating


# read in the csv file as a pandas dataframe
df = pd.read_csv("Netflix_Userbase.csv")

# Build new data frame sos the changes will be not from the original data frame
Netflix = df


# explore the data
print(Netflix.info())

print('#########################################')

# # explore the data shape
print(Netflix.shape)

print('#########################################')

# # explore the data first couple of rows
print(Netflix.head())

print('#########################################')

# # Drop two column that i dont need for investigation of the data set ['index','Date']
# # Netflix.drop(columns=['index','Date','Column1'], axis=1, inplace=True)

# specifying the column names that I want to use
new_cols_dict ={
    'User ID':'User_ID',
    'Subscription Type':'Subscription_Type', 
    'Monthly Revenue':'Monthly_Revenue',
    'Last Payment Date':'Last_Payment_Date',
    'Country':'Country',
    'Age':'Age',
    'Gender':'Gender',
    'Device':'Device',
    'Plan Duration':'Plan_Duration',
}

# # Renaming the columns to the specified column names
Netflix.rename(new_cols_dict, axis=1, inplace=True)


# # explore the data
print(Netflix.info())

print('#########################################')

# # count the unique values in the User_ID column
print(f"Total User count: {Netflix.User_ID.count()}")


print('#########################################')


# # count the unique values in the Country column
print(Netflix.Country.value_counts())

print('#########################################')

# # # count the unique values in the Device column
print(Netflix.Device.value_counts())

print('#########################################')

# # check if ther are null and drop all the rows with missing data
# a = Netflix.dropna(axis=0,inplace=True)
# print(a)

# # explore the data
print(Netflix.info())


# # # writing the final dataframe to an excel file that we will use in our Tableau visualisations. The file will be the 'london_bikes_final.xlsx' file and the sheet name is 'Data'
Netflix.to_excel('Netflix.xlsx', sheet_name='Data', index=False)


