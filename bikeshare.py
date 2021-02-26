import pandas as pd
import numpy as np
import time
import statistics


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'all':'all'}

DATA_TO_MONTH = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June'}

DAY_DATA = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6,'all':'all'}

DATA_TO_DAY = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_name = ''
    while city_name.lower() not in CITY_DATA:
        city_name = input("Which city would you like to analyse? Chicago, New York City, Washington: ")
        if city_name.lower() in CITY_DATA:
            city = CITY_DATA[city_name.lower()]
            continue
        else:
            print("Please, insert a city as specified")

    month_name = ''
    while month_name.lower() not in MONTH_DATA:
        month_name = input("Which month do you want to analyse? January, February, March, April, or June: ")
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
            continue
        else:
            print("Please, insert a month as specified")

    day_name = ''
    while day_name.lower() not in DAY_DATA:
        day_name = input("Which day do you want to analyse? Monday Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday: ")
        if day_name.lower() in DAY_DATA:
            day = day_name.lower()
            continue
        else:
            print("Please, select a day as specified")

    print('-'*40)

    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    start_time = time.time()

    df = pd.read_csv(city)

    df['Start Month'] = pd.DatetimeIndex(df['Start Time']).month

    df['Start Day'] = pd.DatetimeIndex(df['Start Time']).weekday

    df['Start Hour'] = pd.DatetimeIndex(df['Start Time']).hour


    print("\nThis took %s seconds." % (time.time() - start_time))

    return df

def time_stats(df, month, day):

    """Displays statistics on the most frequent times of travel."""

    from statistics import mode

    start_time = time.time()

    top_month = df['Start Month'].dropna()
    top_month = top_month.mode().iat[0]
    print('The most popular month is {}'.format(DATA_TO_MONTH.get(top_month)))

    top_day = df['Start Day'].dropna()
    top_day = top_day.mode().iat[0]
    print('The most popular day is {}'.format(DATA_TO_DAY.get(top_day)))

    top_start_hour = df['Start Hour'].dropna()
    top_start_hour = top_start_hour.mode().iat[0]
    print('The most popular hour is {}'.format(top_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()

    popular_start_station = df['Start Station'].dropna()
    popular_start_station = popular_start_station.mode().iat[0]
    print('The most popular start station is {}'.format(popular_start_station))

    popular_end_station = df['End Station'].dropna()
    popular_end_station = popular_end_station.mode().iat[0]
    print('The most popular end station is {}'.format(popular_end_station))

    df['Trip'] = df[['Start Station', 'End Station']].agg('-'.join, axis=1)
    popular_combination = df['Trip'].mode()[0]
    print('Most Popular Combination: ', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...')

    start_time = time.time()

    df['Trip Duration'] = df['Trip Duration'].fillna(0)

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Statistics...')

    start_time = time.time()

    if 'User Type' in df:
        user_type = df['User Type'].dropna()
        if user_type.empty:
            print('Data not available')
        else:
            user_type = user_type.value_counts()
            print('User type count: {}'.format(user_type))
    if 'Gender' in df:
        user_gender = df['Gender'].dropna()
        if user_gender.empty:
            print('Data not available')
        else:
            user_gender = user_gender.value_counts()
            print('Gender count:{}'.format(user_gender))
    if 'Birth Year' in df:
        birth_year = df['Birth Year'].dropna()
        if birth_year.empty:
            print('Data not available')
        else:
            eldest_user = birth_year.min()
            print('Earliest year of birth : {}'.format(int(eldest_user)))
            youngest_user = birth_year.max()
            print('Most recent year of birth : {}'.format(int(youngest_user)))
            most_common_yob = birth_year.mode().iat[0]
            print('Most common year of birth : {}'.format(int(most_common_yob)))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def raw_data(df):
    """Raw data is shown on user request. A block of five lines is shown"""
    answer = input('Do you want to see the raw data? yes/no : ')
    row_count = 0
    for index, row in df.dropna().iterrows():
        if answer == 'no':
            break
        elif answer == 'yes':
            print(row)
        else:
            print('Please, refer as mentioned')
        row_count += 1
        if row_count != 0 and row_count %5 == 0:
            answer = input('Would you like to see more raw data? yes/no : ')
            if answer == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? [Enter yes or no]:\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
