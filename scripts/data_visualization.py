"""
Week 3: Data Visualization with Matplotlib & Seaborn
Generates analytical charts and figures for the cleaned fitness workout dataset.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations():
    print("=" * 80)
    print("WEEK 3: DATA VISUALIZATION WITH MATPLOTLIB & SEABORN")
    print("=" * 80)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_path = os.path.join(script_dir, "..", "data", "cleaned_data.csv")
    visuals_dir = os.path.join(script_dir, "..", "visuals")
    os.makedirs(visuals_dir, exist_ok=True)
    
    df = pd.read_csv(cleaned_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set styling theme
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams["font.family"] = "sans-serif"
    
    # -------------------------------------------------------------------------
    # Visual 1: Calories vs Duration (Scatter Plot with Regression Trendline)
    # -------------------------------------------------------------------------
    print("\n[Chart 1] Generating Calories vs Duration Scatter Plot...")
    plt.figure(figsize=(8, 5))
    sns.regplot(
        data=df, 
        x="Duration", 
        y="Calories", 
        color="#1F4E79", 
        scatter_kws={"s": 65, "alpha": 0.8},
        line_kws={"color": "#D9534F", "linewidth": 2}
    )
    plt.title("Workout Duration vs. Calories Burned", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Session Duration (Minutes)", fontsize=11)
    plt.ylabel("Total Calories Burned (kcal)", fontsize=11)
    plt.tight_layout()
    p1 = os.path.join(visuals_dir, "calories_vs_duration.png")
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f"-> Saved: {p1}")

    # -------------------------------------------------------------------------
    # Visual 2: Workout Daily Trend throughout December (Timeline Line Plot)
    # -------------------------------------------------------------------------
    print("\n[Chart 2] Generating December Timeline Trend Plot...")
    fig, ax1 = plt.subplots(figsize=(11, 5))
    
    color_cal = "#2E75B6"
    color_pulse = "#E67E22"
    
    ax1.plot(df['Date'].dt.strftime('%b %d'), df['Calories'], marker='o', color=color_cal, linewidth=2, label="Calories (kcal)")
    ax1.set_xlabel("Workout Date (December 2020)", fontsize=11, labelpad=8)
    ax1.set_ylabel("Calories Burned (kcal)", color=color_cal, fontsize=11)
    ax1.tick_params(axis='y', labelcolor=color_cal)
    ax1.set_xticklabels(df['Date'].dt.strftime('%b %d'), rotation=45, ha='right')
    
    ax2 = ax1.twinx()
    ax2.plot(df['Date'].dt.strftime('%b %d'), df['Pulse'], marker='s', color=color_pulse, linewidth=2, linestyle='--', label="Avg Pulse (bpm)")
    ax2.set_ylabel("Average Pulse (bpm)", color=color_pulse, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=color_pulse)
    ax2.grid(False)
    
    plt.title("Daily Calorie Expenditure & Heart Rate Progression (Dec 2020)", fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    p2 = os.path.join(visuals_dir, "workout_trends_december.png")
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f"-> Saved: {p2}")

    # -------------------------------------------------------------------------
    # Visual 3: Pulse & Maxpulse Distribution (KDE and Histogram)
    # -------------------------------------------------------------------------
    print("\n[Chart 3] Generating Pulse Distribution Histogram & KDE...")
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Pulse'], color="#3498DB", kde=True, label="Resting / Avg Pulse", bins=10, alpha=0.6)
    sns.histplot(df['Maxpulse'], color="#E74C3C", kde=True, label="Peak Maxpulse", bins=10, alpha=0.5)
    plt.title("Cardiovascular Pulse vs. Peak Heart Rate Distribution", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Heart Rate (Beats Per Minute - BPM)", fontsize=11)
    plt.ylabel("Session Frequency", fontsize=11)
    plt.legend(frameon=True)
    plt.tight_layout()
    p3 = os.path.join(visuals_dir, "pulse_distribution.png")
    plt.savefig(p3, dpi=300)
    plt.close()
    print(f"-> Saved: {p3}")

    # -------------------------------------------------------------------------
    # Visual 4: Calories by Workout Intensity Category (Boxplot)
    # -------------------------------------------------------------------------
    print("\n[Chart 4] Generating Workout Intensity Boxplot...")
    plt.figure(figsize=(8, 5))
    intensity_order = ["Light Intensity", "Moderate Intensity", "High Intensity"]
    sns.boxplot(
        data=df, 
        x="Workout_Intensity", 
        y="Calories", 
        order=intensity_order, 
        palette=["#A2D2FF", "#BDE0FE", "#FFC8DD"]
    )
    sns.stripplot(
        data=df, 
        x="Workout_Intensity", 
        y="Calories", 
        order=intensity_order, 
        color="#2B2D42", 
        size=7, 
        jitter=0.2, 
        alpha=0.7
    )
    plt.title("Calorie Burn Distribution Across Workout Intensity Tiers", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Engineered Workout Intensity Tier", fontsize=11)
    plt.ylabel("Calories Burned (kcal)", fontsize=11)
    plt.tight_layout()
    p4 = os.path.join(visuals_dir, "workout_intensity_boxplot.png")
    plt.savefig(p4, dpi=300)
    plt.close()
    print(f"-> Saved: {p4}")

    # -------------------------------------------------------------------------
    # Visual 5: Correlation Matrix Heatmap
    # -------------------------------------------------------------------------
    print("\n[Chart 5] Generating Correlation Matrix Heatmap...")
    plt.figure(figsize=(8, 6))
    num_cols = ["Duration", "Pulse", "Maxpulse", "Calories", "Calories_Per_Minute", "Heart_Rate_Spread"]
    corr = df[num_cols].corr()
    
    sns.heatmap(
        corr, 
        annot=True, 
        fmt=".2f", 
        cmap="Blues", 
        square=True, 
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )
    plt.title("Health & Fitness Metrics Correlation Heatmap", fontsize=14, fontweight="bold", pad=14)
    plt.tight_layout()
    p5 = os.path.join(visuals_dir, "correlation_heatmap.png")
    plt.savefig(p5, dpi=300)
    plt.close()
    print(f"-> Saved: {p5}")

    print("\n" + "=" * 80)
    print("ALL 5 VISUALIZATIONS GENERATED AND SAVED TO VISUALS/")
    print("=" * 80)

if __name__ == "__main__":
    generate_visualizations()
