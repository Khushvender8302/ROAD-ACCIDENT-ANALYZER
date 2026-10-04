import pandas as pd
import numpy as np

# 1. Load Dataset
df = pd.read_csv("ROADACCIDENTCASE.csv")

# 2. Check Missing Values & Duplicates
df.drop_duplicates(subset=['Accident_Index'], inplace=True)
df['Weather_Conditions'].fillna('Unknown', inplace=True)

# 3. Date & Time Transformation
df['Accident_Date'] = pd.to_datetime(df['Accident_Date'])
df['Year'] = df['Accident_Date'].dt.year
df['Month'] = df['Accident_Date'].dt.strftime('%b')
df['Day_Name'] = df['Accident_Date'].dt.day_name()

# 4. Standardize Text Columns
df['Accident_Severity'] = df['Accident_Severity'].str.title()
df['Urban_or_Rural_Area'] = df['Urban_or_Rural_Area'].map({1: 'Urban', 2: 'Rural'}).fillna('Other')

# 5. Export Clean Data for SQL / Power BI
df.to_csv('cleaned_road_accidents.csv', index=False)
print("Data Cleaning Complete. Shape:", df.shape)