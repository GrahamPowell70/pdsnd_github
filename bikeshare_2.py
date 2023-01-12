import time
import pandas as pd
#import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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

        #city = ez.choicebox('Please enter city of interest', title='city choice', choices=('Chicago', 'New York City', 'Washington'))

    ok_cities = list(CITY_DATA.keys())

    city = input('Please enter a city. either Chicago, New York City or Washington: ').lower()
    while city not in ok_cities:
        print ("Data not available for this city. ")
        city = input('Please enter a city. either Chicago, New York City or Washington: ').lower()


    # get user input for month (all, january, february, ... , june)
    month = input('Please enter month of interest or all (January to June): ').lower()
    #month = ez.enterbox('Please enter month of interest or all', title='month entry', default='All').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print('Invalid month name ')
        #month = ez.enterbox('Please enter month of interest or all', title='month entry', default='All').lower()
        month = input('Please enter month of interest or all (January to June): ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter day of week (or all): ').lower()
    #day = ez.enterbox('Please enter day of week (or all)', title='day entry', default='All').lower()
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day =input('That isn\'t a day of the week Please enter a valid day (or all): ').lower()
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
    df = pd.read_csv(CITY_DATA[city])
    #convert Start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Extract month and day from Start time
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name() # changed  from weekday_name (pd<0.22) from example to day_name() function

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (if all months are included) or state which month we're looking at
    if len(pd.unique(df['month'])) > 1: #test to see we haven't just got one month
        print('Most popular month of travel= ' + months[df['month'].mode()[0]-1].capitalize())
    else:
        print('Data restricted to ' +month.capitalize()+ ' only')

    # display the most common day of week if all days are included or say what day we're looking at
    if len(pd.unique(df['day'])) > 1:  # test to see we haven't just got one month
        pop_day = str(df['day'].mode()[0])
        print ('Most popular day to travel in '+ month.capitalize() + ' = ' + pop_day)
    else:
        print('data filtered to '+ day.capitalize() + "'s only")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    am_pm = 'am'
    # Make output easier to read by formatting hour to am/pm
    if most_popular_hour >= 12:
        am_pm = 'pm'
    if most_popular_hour >= 13:
        most_popular_hour -= 12
    print ('Most popular departure hour = ' +str(most_popular_hour) +' '+ am_pm)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('Most Commonly used Starting station= ' + df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Commonly used end station= ' + df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['trips'] = df["Start Station"] + ' to ' + df["End Station"]
    print('Most common trip= ' + df['trips'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # df['travel time']= df['End Time'] - df['Start Time']
    # print (df['travel time'])
    # Argh. These are already in the data as Trip Duration

    # display total travel time
    total_time = df['Trip Duration'].sum()
    hours, minutes, seconds = hours_minutes_seconds(total_time)


    print('Total time for all journeys = {:.2f} seconds'.format(total_time) )
    print( ' = {}  hours, {} minutes, {:.2f} seconds'.format(hours, minutes, seconds))


    # display mean travel time
    average_journey_time = df['Trip Duration'].mean()
    print( 'average journey time for all trips in selected month/day = {:.2f} minutes'.format(average_journey_time/60))


    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)

def hours_minutes_seconds(time_in_s):

    """Just returns hours, minutes and seconds from a number of seconds"""
    hours = int(time_in_s/3600)
    minutes = int((time_in_s%3600)/60)
    seconds = time_in_s%60
    return hours, minutes, seconds



def user_stats(df):
    """Displays statistics on bikeshare users."""

# Washington is short on Gender and birthyear. Need general test for completeness of data

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type counts= ')
    print('-'*40)
    print(df.groupby('User Type')['User Type'].count())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('-' * 40)
        print('Gender Counts:')
        print(df.groupby('Gender')['Gender'].count())
    else:
        print('No Gender information in this dataset')

    # Display earliest, most recent, and most common year of birth
    print('-' * 40)
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_frequent = int(df['Birth Year'].mode())
        print('Earliest birth year of travelers = {}, Most recent birth year = {} and the most common birth year = {}'
              .format(earliest, most_recent, most_frequent))
    else:
        print('No Birth year information in this dataset')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(data):
    answer = input('Would you like to print the first five rows of data (yes/no)? ')
    rows = 0
    #Only print out the original, relevant columns 1 to 8, the rest have been generated from this data for calculations

    while answer.lower() != 'no':
        print(data.iloc[rows:rows+5, 1:8].to_string())
        rows += 5
        answer = input('Would you like to print the next five rows of data (yes/no)? ')
    #print(data.iloc[5:10])

def wait_for_enter():
    """Waits for enter to be pressed before continuing"""
    input("Press enter to continue")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        wait_for_enter()
        station_stats(df)
        wait_for_enter()
        trip_duration_stats(df)
        wait_for_enter()
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        restart = restart[0]
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
