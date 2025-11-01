def main():
    print("Bikeshare script is running...")

if __name__ == "__main__":
    main()# Project: Bikeshare
# This file loads local CSVs and prints simple info.



import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print("Hello! Let's explore some US bikeshare data!")

    city = ''
    while city not in CITY_DATA:
        city = input("Choose a city (Chicago, New York City, Washington): ").strip().lower()
        if city not in CITY_DATA:
            print("Invalid city. Please enter: Chicago, New York City, or Washington.")

    month = ''
    while month not in VALID_MONTHS:
        month = input("Filter by month? (all, January, February, March, April, May, June): ").strip().lower()
        if month not in VALID_MONTHS:
            print("Invalid month. Please choose from: all, January–June.")

    day = ''
    while day not in VALID_DAYS:
        day = input("Filter by day? (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ").strip().lower()
        if day not in VALID_DAYS:
            print("Invalid day. Please choose a correct day name or 'all'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_to_num = {
            'january': 1, 'february': 2, 'march': 3,
            'april': 4, 'may': 5, 'june': 6
        }
        df = df[df['month'] == month_to_num[month]]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def most_common(series):
    """Safe mode (returns None if series empty)."""
    if series.empty:
        return None
    return series.mode(dropna=True).iloc[0]


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month_num = most_common(df['month'])
    common_month = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}.get(common_month_num, None)
    common_day = most_common(df['day_of_week'])
    common_hour = most_common(df['hour'])

    print(f"Most common month: {common_month if common_month else 'N/A'}")
    print(f"Most common day of week: {common_day if pd.notna(common_day) else 'N/A'}")
    print(f"Most common start hour: {common_hour if pd.notna(common_hour) else 'N/A'}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start = most_common(df['Start Station'])
    common_end = most_common(df['End Station'])

    if not df.empty:
        combo = (df['Start Station'] + " -> " + df['End Station'])
        common_trip = most_common(combo)
    else:
        common_trip = None

    print(f"Most commonly used start station: {common_start if pd.notna(common_start) else 'N/A'}")
    print(f"Most commonly used end station: {common_end if pd.notna(common_end) else 'N/A'}")
    print(f"Most frequent trip: {common_trip if pd.notna(common_trip) else 'N/A'}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def format_duration(seconds):
    """Return human-readable duration from seconds."""
    if pd.isna(seconds):
        return 'N/A'
    seconds = int(seconds)
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    if secs or not parts: parts.append(f"{secs}s")
    return ' '.join(parts)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_sec = df['Trip Duration'].sum() if not df.empty else np.nan
    mean_sec = df['Trip Duration'].mean() if not df.empty else np.nan

    print(f"Total travel time: {format_duration(total_sec)} ({int(total_sec) if pd.notna(total_sec) else 'N/A'} seconds)")
    print(f"Average travel time: {format_duration(mean_sec)} ({int(mean_sec) if pd.notna(mean_sec) else 'N/A'} seconds)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' in df.columns and not df['User Type'].empty:
        print("Counts of user types:")
        print(df['User Type'].value_counts(dropna=False).to_string())
    else:
        print("User Type data not available.")

    if 'Gender' in df.columns:
        print("\nCounts of gender:")
        print(df['Gender'].value_counts(dropna=False).to_string())
    else:
        print("\nGender data not available for this city.")

    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year'].dropna()
        if not birth_years.empty:
            earliest = int(birth_years.min())
            most_recent = int(birth_years.max())
            most_common_year = int(birth_years.mode().iloc[0])
            print("\nBirth year stats:")
            print(f"Earliest: {earliest}")
            print(f"Most recent: {most_recent}")
            print(f"Most common: {most_common_year}")
        else:
            print("\nBirth year stats not available (all values missing).")
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# <<< NEW: put this OUTSIDE of user_stats, with no leading spaces before 'def'
def display_raw_data(df):
    """
    Displays 5 lines of raw data at a time upon user request.
    Keeps showing next 5 lines until user says 'no' or data ends.
    """
    base_cols = [
        'Start Time', 'End Time', 'Trip Duration',
        'Start Station', 'End Station', 'User Type',
        'Gender', 'Birth Year'
    ]
    cols = [c for c in base_cols if c in df.columns]

    i = 0
    while True:
        show_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no:\n").strip().lower()
        if show_data != 'yes':
            break
        print(df[cols].iloc[i:i+5].to_string(index=False))
        i += 5
        if i >= len(df):
            print("\nNo more data to display.")
            break
# >>> END NEW


import os

if not os.path.exists("chicago.csv"):
    print("[warn] chicago.csv not found — place CSVs next to bikeshare.py")
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)   # show raw rows on demand

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.strip().lower() != 'yes':
            break


from typing import Optional

def top_station(csv_path: str, column_name: str = "Start Station") -> Optional[str]:
    # TODO: implement
    return None


if __name__ == "__main__":
    main()
