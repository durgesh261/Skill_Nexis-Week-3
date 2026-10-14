"""
Week 3: Python & Data Wrangling
Assignment: Clean a messy dataset in Pandas (handle missing values, filter rows, create new columns)
Dataset: dirty_data.csv (Fitness / Workout tracking records)
"""

import os
import pandas as pd
import numpy as np

def clean_and_wrangle_data():
    print("=" * 80)
    print("WEEK 3: PYTHON & DATA WRANGLING — DATA CLEANING PIPELINE")
    print("=" * 80)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(script_dir, "..", "data", "dirty_data.csv")
    cleaned_path = os.path.join(script_dir, "..", "data", "cleaned_data.csv")
    
    # -------------------------------------------------------------------------
    # Step 1: Load the messy dataset and inspect issues
    # -------------------------------------------------------------------------
    print("\n[Step 1] Loading messy dataset...")
    df_raw = pd.read_csv(raw_path)
    print(f"Raw Dataset Shape: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
    print("\nInitial Raw Data (Head 10):")
    print(df_raw.head(10))
    
    print("\nMissing Values Audit (Before Cleaning):")
    print(df_raw.isnull().sum())
    
    print(f"\nDuplicate Rows (Before Cleaning): {df_raw.duplicated().sum()}")
    
    df = df_raw.copy()
    
    # -------------------------------------------------------------------------
    # Step 2: Handle Date formatting and Missing Dates
    # -------------------------------------------------------------------------
    print("\n[Step 2] Cleaning and standardizing 'Date' column...")
    # Clean quotes around dates if present
    df['Date'] = df['Date'].astype(str).str.replace("'", "").str.strip()
    
    # Inspect empty or 'nan' string in Date
    missing_date_mask = df['Date'].isna() | df['Date'].isin(['', 'nan', 'None'])
    print(f"Rows with missing Date: {missing_date_mask.sum()}")
    
    # Impute missing date using sequential calendar logic (row 22 is between Dec 21 and Dec 23)
    df.loc[missing_date_mask, 'Date'] = '2020-12-22'
    print("-> Imputed missing Date with '2020-12-22'.")
        
    # Convert 'Date' to proper datetime object (handles 20201226 and 2020/12/01 uniformly)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    print("-> Successfully converted 'Date' column to standard datetime (YYYY-MM-DD).")
    
    # -------------------------------------------------------------------------
    # Step 3: Handle Outliers and Incorrect Values in 'Duration'
    # -------------------------------------------------------------------------
    print("\n[Step 3] Detecting and correcting outliers in 'Duration'...")
    # Row 7 has Duration = 450 (data entry typo for 45)
    outliers = df[df['Duration'] > 120]
    print(f"Outlier records detected in Duration (> 120 min):\n{outliers}")
    
    # Correct 450 to 45
    df.loc[df['Duration'] == 450, 'Duration'] = 45
    print("-> Corrected 'Duration' outlier 450 to 45 min.")
    
    # -------------------------------------------------------------------------
    # Step 4: Handle Missing Values in 'Calories'
    # -------------------------------------------------------------------------
    print("\n[Step 4] Handling missing values in 'Calories'...")
    missing_cal_count = df['Calories'].isnull().sum()
    print(f"Missing Calories count: {missing_cal_count}")
    
    # Impute missing Calories with median grouped by Duration
    duration_cal_median = df.groupby('Duration')['Calories'].transform('median')
    df['Calories'] = df['Calories'].fillna(duration_cal_median)
    # If any remaining, fill with global median
    df['Calories'] = df['Calories'].fillna(df['Calories'].median())
    df['Calories'] = df['Calories'].round(1)
    print("-> Imputed missing Calories using duration-specific median values.")

    # -------------------------------------------------------------------------
    # Step 5: Remove Duplicates
    # -------------------------------------------------------------------------
    print("\n[Step 5] Handling duplicate records...")
    initial_len = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"-> Removed {initial_len - len(df)} duplicate row(s). Final row count: {len(df)}")
    
    # -------------------------------------------------------------------------
    # Step 6: Create New Engineered Columns (Feature Engineering)
    # -------------------------------------------------------------------------
    print("\n[Step 6] Creating new analytical columns...")
    
    # 1. Calories per Minute
    df['Calories_Per_Minute'] = (df['Calories'] / df['Duration']).round(2)
    
    # 2. Heart Rate Reserve (Maxpulse - Pulse)
    df['Heart_Rate_Spread'] = df['Maxpulse'] - df['Pulse']
    
    # 3. Workout Intensity Category based on Pulse & Calories per minute
    conditions = [
        (df['Pulse'] >= 110) | (df['Calories_Per_Minute'] >= 6.0),
        (df['Pulse'] >= 100) & (df['Pulse'] < 110),
        (df['Pulse'] < 100)
    ]
    choices = ['High Intensity', 'Moderate Intensity', 'Light Intensity']
    df['Workout_Intensity'] = np.select(conditions, choices, default='Moderate Intensity')
    
    # 4. Day of the Week
    df['Day_Name'] = df['Date'].dt.day_name()
    
    # 5. Weekend Indicator
    df['Is_Weekend'] = df['Date'].dt.dayofweek.isin([5, 6])
    
    print("-> Created 5 new features: ['Calories_Per_Minute', 'Heart_Rate_Spread', 'Workout_Intensity', 'Day_Name', 'Is_Weekend']")
    
    # -------------------------------------------------------------------------
    # Step 7: Row Filtering Demonstrations (Assignment Requirement)
    # -------------------------------------------------------------------------
    print("\n[Step 7] Demonstrating analytical row filtering...")
    
    # Filter A: High Calorie Workouts (> 300 kcal)
    high_cal = df[df['Calories'] > 300]
    print(f"Filter A - High Calorie Workouts (> 300 kcal): {len(high_cal)} sessions")
    
    # Filter B: Extended Cardio Workouts (Duration >= 60 min)
    long_sessions = df[df['Duration'] >= 60]
    print(f"Filter B - Sessions >= 60 minutes: {len(long_sessions)} sessions")
    
    # Filter C: High Peak Heart Rate (Maxpulse >= 140 bpm)
    peak_hr = df[df['Maxpulse'] >= 140]
    print(f"Filter C - Peak Heart Rate (Maxpulse >= 140): {len(peak_hr)} sessions")
    
    # -------------------------------------------------------------------------
    # Step 8: Save Cleaned and Enriched Dataset
    # -------------------------------------------------------------------------
    df.to_csv(cleaned_path, index=False)
    print(f"\n[Step 8] Cleaned dataset saved successfully to: {cleaned_path}")
    print(f"Final Cleaned Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nFinal Cleaned Data Sample (Top 5):")
    print(df.head())
    
    print("\n" + "=" * 80)
    print("DATA CLEANING PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    return df

if __name__ == "__main__":
    clean_and_wrangle_data()
