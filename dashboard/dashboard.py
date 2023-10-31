import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
rental_daily_df = pd.read_csv('dashboard/day.csv')
rental_hourly_df = pd.read_csv('dashboard/hour.csv')


# Function to get daily bike rentals vs temperature data
def get_daily_bike_rentals_vs_temperature_data(df):
    t_max = 39
    t_min = -8
    df['temp_celcius'] = df['temp'] * (t_max - t_min) + t_min
    return df

# Function to get daily bike rentals vs working day data
def get_daily_bike_rentals_vs_working_day_data(df):
    sum_working_day_rental_daily_df = df.groupby('workingday')['cnt'].sum().reset_index()
    sum_working_day_rental_daily_df['workingday'] = sum_working_day_rental_daily_df['workingday'].replace({0: 'Non-Working Day', 1: 'Working Day'})
    return sum_working_day_rental_daily_df

# Function to get daily bike rentals over the years data
def get_daily_bike_rentals_over_the_years_data(df):
    df['year'] = df['yr'].replace({0: 2011, 1: 2012})
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year'] = df['dteday'].dt.year
    return df

# Function to get daily bike rentals vs season data
def get_daily_bike_rentals_vs_season_data(df):
    sum_season_rental_daily_df = df.groupby('season')['cnt'].sum().reset_index().sort_values(by='cnt', ascending=False)
    sum_season_rental_daily_df['season'] = sum_season_rental_daily_df['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return sum_season_rental_daily_df

# Define the Streamlit app
st.title("Bike Sharing Data Analysis")

# Sidebar for data selection
with st.sidebar:
    # Title
    st.title("Aditya Dharma Mulyatama")

    # Logo Image
    st.image("logo.png")


# Visualize the data
st.write("### Daily Bike Rentals vs Temperature")
daily_bike_rentals_vs_temperature_df = get_daily_bike_rentals_vs_temperature_data(rental_daily_df)
fig, ax = plt.subplots(figsize=(10, 5))
sns.set(style='whitegrid')
sns.scatterplot(x='temp_celcius', y='cnt', data=daily_bike_rentals_vs_temperature_df, ax=ax, palette='coolwarm',hue='temp_celcius',legend=False)
ax.set(xlabel='Temperature (°C)', ylabel='Number of Bike Rentals')
st.pyplot(fig)

# Explore the data further
st.write("### Daily Bike Rentals vs Working Day")
daily_bike_rentals_vs_working_day_df = get_daily_bike_rentals_vs_working_day_data(rental_daily_df)
fig, ax = plt.subplots(figsize=(10, 5))
plt.figure(figsize=(10, 5))
sns.set(style='whitegrid')
sns.barplot(x='workingday', y='cnt', data=daily_bike_rentals_vs_working_day_df,ax=ax,palette='pastel',ci=None)
plt.xlabel('Working Day')
plt.ylabel('Number of Bike Rentals')
plt.title('Daily Bike Rentals vs Working Day')
st.pyplot(fig)

st.write("### Daily Bike Rentals Over the Years")
fig, ax = plt.subplots(figsize=(10, 5))
daily_bike_rentals_over_the_years_df = get_daily_bike_rentals_over_the_years_data(rental_daily_df)
sns.set(style='darkgrid')
sns.lineplot(x='dteday', y='cnt', data=daily_bike_rentals_over_the_years_df, palette='muted', hue='year', ax=ax)
ax.set(xlabel='Date', ylabel='Number of Bike Rentals')
plt.xticks(rotation=45)
st.pyplot(fig)

st.write("### Daily Bike Rentals vs Season")
daily_bike_rentals_vs_season_df = get_daily_bike_rentals_vs_season_data(rental_daily_df)
highest_season = daily_bike_rentals_vs_season_df.iloc[0]['season']
fig, ax = plt.subplots(figsize=(10, 5))
sns.set(style='whitegrid')
sns.barplot(x='season', y='cnt', data=daily_bike_rentals_vs_season_df, hue='season',
            palette=['darkblue' if x == highest_season else '#D3D3D3' for x in daily_bike_rentals_vs_season_df['season']],
            order=daily_bike_rentals_vs_season_df['season'], ax=ax)
ax.set(xlabel='Season', ylabel='Number of Bike Rentals')
st.pyplot(fig)

st.write("## Conclusion")
st.write("Based on the analysis, we can make the following conclusions:")
st.write("- There is a strong positive correlation between temperature and the number of bike rentals.")
st.write("- More bikes are rented on working days compared to non-working days.")
st.write("- Bike rentals increased from 2011 to 2012.")
st.write("- The highest number of bike rentals occurs during the fall season.")

st.caption("Copyright (C) Aditya Dharma Mulyatama")

