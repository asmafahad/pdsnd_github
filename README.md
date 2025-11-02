# Bikeshare Project

This repository contains a simple Python script (`bikeshare.py`) for exploring bikeshare data locally.  
CSV files are ignored via `.gitignore` and should not be pushed to GitHub.

## Description
This project analyzes data from bikeshare systems in Chicago, New York City, and Washington.  
It allows the user to filter data by city, month, and day, and then computes statistics such as:
- The most common times of travel.
- The most popular stations and trips.
- The total and average trip duration.
- User types and demographics (when available).

## How to Run
1. Place the CSV data files in the same folder as `bikeshare.py` (these files are **ignored by Git**).
2. Run the script using:
   ```bash
   python3 bikeshare.py
