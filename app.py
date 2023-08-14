import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px


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

# loading data
data = load_data(100000)
original_data = data


# displaying data in a map
st.header('Where are the most people injured in NYC')
injured_people = st.slider('Number of persons injured',0,19)
st.map(data.query('injured_persons >= @injured_people')[['latitude', 'longitude']].dropna(how='any') )
 
st.header("How many collisions occur during a give time of the day")
hour = st.slider('Hour to look at', 0, 23)
data = data[data['date/time'].dt.hour == hour]


# 3D plot
st.markdown(f'vehicle collision between {hour}:00 and {hour + 1}:00')
# creating map
midpoint = (np.average(data['latitude']), np.average(data['longitude']))
st.write(pdk.Deck(
    map_style= "mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data = data[['date/time','latitude','longitude']],
        get_position = ['longitude', 'latitude'],
        radius = 100,
        extruded = True,
        pickable = True,
        elevation_scale = 4,
        elevation_range = [0, 1000],
        ),
    ],
))


# chart and histograms
st.subheader(f"Breakdown by minute between {hour}:00 and {hour + 1}:00")
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour+1))
    ]
hist,bin_edge = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))
chart_data = pd.DataFrame({"minute":range(60),"crashes":hist})
fig = px.bar(chart_data, x="minute", y="crashes", hover_data=['minute','crashes'], height=400)
st.write(fig)


# dropdown
st.header('Top 5 dangerous streets by affected type')
select = st.selectbox('Affected type of people', options=['Pedestrians','Cyclists','Motorists'])

if select == "Pedestrians":
    st.write(original_data.query("injured_pedestrians >=1 ")[["on_street_name", "injured_pedestrians"]].sort_values(by="injured_pedestrians",ascending=False).dropna(how="any").head())
elif select == "Cyclists":
    st.write(original_data.query("injured_cyclists >=1 ")[["on_street_name", "injured_cyclists"]].sort_values(by="injured_cyclists",ascending=False).dropna(how="any").head())
else:
    st.write(original_data.query("injured_motorists >=1 ")[["on_street_name", "injured_motorists"]].sort_values(by="injured_motorists",ascending=False).dropna(how="any").head())


# checkbox to show data
if st.checkbox("Show Raw data"):
    
    # subheading for the load_data
    st.subheader("Raw data")

    # loading data
    st.write(data)
