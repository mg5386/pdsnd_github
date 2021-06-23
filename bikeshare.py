import time
import pandas as pd
import numpy as np

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
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
            if city in ['chicago', 'new york city', 'washington']:
                break
            else:
                print('Please enter a valid city')
        except:
            print('Please enter a valid city')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('The available data exists for months January through June.\nIf you want to see the data for a given month, enter it next. Otherwise enter "all"\n').title()
            if month in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
                break
            else:
                print('Please enter a valid month')
        except:
            print('Please enter a valid month')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('If you want to see the data for a given day of the week, enter it next. Otherwise enter "all"\n').title()
            if day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','All']:
                break
            else:
                print('Please enter a valid day of the week')
        except:
            print('Please enter a valid day of the week')


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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #address missing Birth Year data so we can convert to int
    if 'Birth Year' in df.columns:
        #replace missing values with most common birth year
        common_year = df['Birth Year'].mode()[0]
        df['Birth Year'].fillna(common_year, inplace=True)
        df['Birth Year'] = df['Birth Year'].astype(int)

    # extract data from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    months = {1:'January', 2:'February', 3:'March', 4: 'April', 5: 'May', 6: 'June'}
    print('\nThe most common month in this city is {}'.format(months[popular_month]))

    popular_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week in this city is {}'.format(popular_day))
    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    print('\nThe most common start hour in this city is {}'.format(popular_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    #concatenating strings to make it easier to read for the user
    df['trip'] = 'from the ' + df['Start Station'] + ' station to the ' + df['End Station'] + ' station'
    popular_trip = df['trip'].mode()[0]
    print('\nThe most frequent trip is {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time (in minutes): ',total_travel_time)
    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time (in minutes): ',round(avg_travel_time,2)) #using round to make it easier to read

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUser type distribution:\n\n', df['User Type'].value_counts())

    # Display counts of gender
    #since Gender is not found in all datasets:
    if 'Gender' in df.columns:
        print('\nGender distribution:\n\n', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    #since Birth Year is not found in all datasets:
    if 'Birth Year' in df.columns:
        print('\nYear of birth details:')
        print('\nEarliest:', df['Birth Year'].min())
        print('\nMost recent:', df['Birth Year'].max())
        print('\nMost common:', df['Birth Year'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """ Displays original data for 5 trips at a time if the user so chooses """
    i = 0
    raw = input("\nWould you like to view individual trip data? Type 'yes' or 'no'\n").lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)
    #remove the columns we had created to help calculate stats so only original trip data is shown
    df = df.iloc[:,:-4]
    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            #printing without index to improve presentation
            print(df[i:i+5].to_string(index=False)) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("\nWould you like to view individual trip data? Type 'yes' or 'no'\n").lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
