import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

def get_user_input(message,options):
    '''
    A function that validates user input.
    Args:
        (str) message - Message asking for user to choose a valid option
        (list) options - List of valid options
    '''
    while (True):
        user_input = input(message)
        if user_input.lower() in options:
            return user_input.lower()
        else:
            print('\nNot a valid option. Please try again.\n')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    message = 'Please choose a city, Chicago, New York City or Washington:\n'
    city = get_user_input(message, CITY_DATA)

    # get user input for month (all, january, february, ... , june)
    message = 'Please choose a month, all, January, February,...June:\n'
    month = get_user_input(message, months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    message = 'Please choose a day of the week, all, Monday, Tuesday... Sunday \n'
    options = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = get_user_input(message, options)

    print('-'*40)
    return city, month, day

def chunker(iterable, size):
    """Yield successive chunks from iterable of length size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def print_raw_data(df):
    '''
    Function that print 5 trips in our dataset
    '''
    message = 'Would you like to view trip data? yes/no\n'
    options = ['yes','y','no','n']
    user_input = get_user_input(message,options)
    if user_input == 'yes' or user_input == 'y':
        for chunk in chunker(df,5):
            print(chunk)
            user_input = get_user_input(message,options)
            if user_input == 'n' or user_input == 'no':
                break

def column_exists(column_name,df):
    '''
    Function that tests to see if a column exists in a pandas dataframe
    '''
    return column_name in df

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = pd.Series(df['Start Time'].dt.month)
    df['day_of_week'] = pd.Series(df['Start Time'].dt.weekday_name)
    if month != 'all':
        df = df[df['month'] == months.index(month)]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    df.fillna(method = 'backfill', axis = 0)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if column_exists('Start Time', df):
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        pop = months[df['month'].mode()[0]].title()
        print("The most popular month was {}.".format(pop))

        # display the most common day of week
        pop = df['day_of_week'].mode()[0]
        print("The most popular day was {}.".format(pop))
        
        # display the most common start hour
        df['hour'] = pd.Series(df['Start Time'].dt.hour)
        pop = df['hour'].mode()[0]
        print("The most popular starting hour was {}.".format(pop))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    if column_exists('Start Station', df) and column_exists('End Station', df):
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()
        # display most commonly used start station

        pop = df['Start Station'].mode()[0]
        print('The most popular stating station was {}.'.format(pop))

        # display most commonly used end station
        pop = df['End Station'].mode()[0]
        print('The most popular ending station was {}.'.format(pop))

        # display most frequent combination of start station and end station trip
        df['trip'] = pd.Series(df['Start Station'] + ' to ' + df['End Station'])
        pop = df['trip'].mode()[0]
        print('The most popular trip was {}.'.format(pop))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if column_exists('End Time', df) and column_exists('Start Time', df):
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display total travel time
    
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['travel_time'] = pd.Series(df['End Time'] - df['Start Time'])
    
        print('Total travel time was {}.'.format(df['travel_time'].sum()))
    
        # display mean travel time
        print('The mean travel time is {}.'.format(df['travel_time'].mean()))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    if column_exists('User Type', df) or column_exists('Gender', df) or column_exists('Birth Year', df):
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        if column_exists('User Type', df):
            print('User Types:\n{}\n'.format(df['User Type'].value_counts()))

        # Display counts of gender
        if column_exists('Gender', df):
            print('Gender:\n{}\n'.format(df['Gender'].value_counts()))

        # Display earliest, most recent, and most common year of birth
        if column_exists('Birth Year', df):
            early = int(df['Birth Year'].min())
            print('The earliest recorded year of birth is {}'.format(early))
            
            recent = int(df['Birth Year'].max())
            print('The most recent recorded year of birth is {}'.format(recent))
            
            pop = int(df['Birth Year'].mode()[0])
            print('The most popular year of birth is {}'.format(pop))
        
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
