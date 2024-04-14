import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    ## Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('_'*80)
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    while True:
         cities = ['chicago','new york', 'washington' ]
         city = input("\n Which city would you like to analyse? (input either chicago , new york or washington)\n").lower()
         try:
              city_input = str(city)
              if city_input in cities:
                   break
              else:
                   print("Opps, Sorry! it looks like we don\'t have this city in our database. Please try again.")
            
         except ValueError:
              print("Opps, Invalid input! please enter a valid city name.")
    # Get user input for month (all, january, february, ... , june).
    while True:
         month = input(" which month would like to explore? Enter all if you'd like to explore all six months :").lower()
         months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
         if month in months:
              break
         else:
              print("\n Opps, It looks like we don\'t have the data for this month. please enter a specific month or all to apply no filter.")
    

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    while True:
         day = input("Please specify a specific day or enter all for no filter:").lower()
         days = ['monday', 'tuesday', 'wenesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
         if day in days:
              break
         else:
              print("please enter a valid day of a week or enter all to daiplay all days:")
        

    print('-'*80)
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
    # First we load the date into dataframe.
    df = pd.read_csv(CITY_DATA[city])
    # Convert start time into datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month,day and hour from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # Filter by month if applicable.
    if month != 'all':
         months = ['january', 'february', 'march', 'april', 'may', 'june']
         # Use month index to get the corresponding integer for each month.
         month = months.index(month)+1

        # Now filter by month if applicable.
         df = df[df['month']== month]
     # Filter by weekday if applicable.
    if day != 'all':
         df = df[df['day_of_week']==day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    common_month = df['month'].mode()[0]
    print("The most common month from the filtered data set is : {}".format(common_month))   

    # Display the most common day of week.
    common_day = df['day_of_week'].mode()[0]
    print("The busiest day from the filtered data set is : {}".format(common_day))

    # Display the most common start hour.
    common_hour = df['hour'].mode()[0]
    print("The busiest hour from the filtered data set is : {}".format(common_hour))

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most used start station is {common_start_station}")




    # Display most commonly used end station.
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is {common_end_station}")


    # Display most frequent combination of start station and end station trip.
    most_frequent_combination = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print(f"The most frequent combination of start and end stations is {most_frequent_combination}")


    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_travel_time = df['Trip Duration'].sum()
    hour, remain_minute = divmod(total_travel_time, 60)
    minute, seconds = divmod(remain_minute, 60)

    print(f"The total travel time  is {total_travel_time} mins, which equals {hour.round(0)} hours, {minute.round(0)} mins and {seconds.round(0)} sec.")


    # Display mean travel time.
    mean_travel_time = df['Trip Duration'].mean().round(1)
    
    h, remain_m = divmod(mean_travel_time, 60)
    m, s = divmod(remain_m, 60)
    print(f"The mean travel time for this data set is {mean_travel_time} min, which equals {h.round(0)} hours, {m.round(0)} mins and {s.round(0)} sec.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_count = df['User Type'].value_counts()
    print("The number of users is \n", user_count)
    
    # Display counts of gender.
    # If statement should be used to avoid any errors as gender stats aren't available in washington.csv file.
    if city.lower() != 'washington' :
         gender = df['Gender'].value_counts()
         print("The number of each gender \n", gender)

    # Display earliest, most recent, and most common year of birth.
         earliest_birth_year = df['Birth Year'].min()
         print(f"The earliest year of birth from selected data is {earliest_birth_year}")
         most_recent_year = df['Birth Year'].max()
         print(f"The most recent year of birth from the selected data is {most_recent_year}")
         most_common_year = df['Birth Year'].mode()[0]
         print(f"Most users are born in {most_common_year}")
    



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def get_plots(df,month):
    ''' Generate a plot showing the number of users over time.
        Uses resample as this involves data time series to get the frequency and aggrergate the data using count().

    '''
    # Plot the number of users over time.
    print("\n Plotting in progress...")
    # First we load the data.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df.set_index('Start Time', inplace=True)
         
    # Depending on the user input in months, time in the x-axis will change from months to days.
    if month.lower() == 'all':
         # Resample the data to monthly frequency and count number of users each month.
         user_count_over_time = df.resample('M')['User Type'].count()
         x_label = 'Month'

    else:
         # Resample the data to daily frequency and count number of users each day.
         user_count_over_time = df.resample('D')['User Type'].count()
         x_label = f'Day in {month}'




    # Plotting...
    
    plt.figure(figsize=(12,6))
    plt.plot(user_count_over_time, marker='o', linestyle='-')
    # Adding title and axis title .
    plt.title('Number of Users Over Time')
    plt.xlabel(x_label)
    plt.ylabel('Number of Users')
    # Change the rotation angle of x-axis ticks to make them fit and more readable.
    plt.xticks(rotation=30)
    plt.grid(True)
    plt.show()
    

def display_data(df):
    '''Upon the user response, displays 10 rows of the filtered data set.
    The user is then asked again if they would like more 10 rows of data.
    '''
    start_time = time.time()
    print(" Displaying raw data...")
    response_list = ['yes', 'no', 'customize']
    while True:
        view_data = input("\nWould you like to view the first ten rows from the filtered data set? Please enter Yes or No.\n else if you would like to customize enter 'customize'.")
        start_loc = 0
        end_loc = 10
        if view_data.lower() in response_list:
            if view_data.lower() == 'yes':
                data = df.iloc[start_loc: end_loc]
                print(data)
                break
            elif view_data.lower() == 'customize':
                 try:
                   start_loc = int(input("please enter starting row: ")) + 1
                   end_loc = int(input ("please enter the final row number: ")) +1
                   data = df.iloc[start_loc : end_loc]
                   print(data)
                   break
                 except ValueError:
                     print( "\n Opps, Invalid input! please enter your selected row numbers")
            else:
                break
        else:
            print("Sorry! I couldn't read that. Please enter either 'yes' , 'no' or 'customize'.")
    
    while True:
        view_extra = input("\nWould you like to view ten more rows from the selected data set? Please enter 'yes' or 'no'.\n ")
        if view_extra.lower() in response_list:
            if view_extra.lower() == 'yes':
                start_loc += 10
                end_loc += 10
                extra = df.iloc[start_loc: end_loc]
                print(extra)
            else:
                break
        else:
            print("Sorry! I couldn't read that. Please enter either 'yes' or 'no'.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("_"*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        ask_for_plots = input("\n would like to plot number of users over time? ")
        if ask_for_plots.lower() == 'yes':
            get_plots(df, month)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
 

if __name__ == "__main__":
	main()
