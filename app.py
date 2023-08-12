import streamlit as st
import pandas as pd
import numpy as np

# url (location in case working locally)
DATA_URL = (
    "Motor_Vehicle_Collisions_-_Crashes.csv"
)

# Main heading
st.title('Motor_Vehicle_Collisions in New York City')

# subheading
st.markdown('This application is a Streamlit dashboard that can be used to anlyse motor vehicle collisions in NYC 🗽💥🚘')

# function to load the data
@st.cache_data(persist=True) # to cache the loaded data, so that we don't need to do this computation everytime we run the app or code or input is changed
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])
    
    # streamlit can't do the mapping if there is any missing values
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    
    # renaming column name to lowercase
    lower = lambda x: str(x).lower()
    data.rename(lower, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    
    return data

data = load_data(100000)

# checkbox to show data
if st.checkbox("Show Raw data"):
    
    # subheading for the load_data
    st.subheader("Raw data")

    # loading data
    st.write(data)
