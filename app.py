# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gLKVVL9BEM9Iza-8R1YMa35zlXvCetcP
"""

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

# Load the dataset
import gdown
url = 'YOUR_GOOGLE_DRIVE_FILE_URL'
output = 'GHED_data.xlsx'
gdown.download(url, output, quiet=False)
file_path = output
df = pd.read_excel(file_path)
import urllib.request
url = '"C:\Users\parth\Downloads\GHED_data.XLSX"'
output = 'GHED_data.xlsx'
urllib.request.urlretrieve(url, output)
file_path = output

# Initial Data Exploration
print("First few rows of the dataset:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nMissing values in each column:")
print(df.isnull().sum())

"""# Data preprocessing"""

# Data Cleaning and Preprocessing
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from scipy.stats import zscore

# Initial Inspection of the Data
print("Initial Data Shape:", df.shape)
print("Data Types and Non-Null Counts:")
print(df.info())
print("\nSummary Statistics:")
print(df.describe(include='all'))

# Checking for Missing Values
print("\nMissing Values in Each Column:")
print(df.isnull().sum())

# Dropping Columns with High Missing Values
# Setting a threshold to drop columns with more than 50% missing values
threshold = 0.5 * len(df)
df = df.dropna(thresh=threshold, axis=1)

# Removing Duplicate Rows
df = df.drop_duplicates()

# Handling Missing Values
# Impute missing values in 'che' based on mean within each income group
df['che'] = df.groupby('income')['che'].transform(lambda x: x.fillna(x.mean()))

# Impute other missing values using interpolation and regional/income group means
df['gghed'] = df['gghed'].interpolate(method='linear')
df['pvtd'] = df['pvtd'].interpolate(method='linear')
df['gghed_pc_usd'] = df.groupby(['region', 'income'])['gghed_pc_usd'].transform(lambda x: x.fillna(x.mean()))
df['pvtd_pc_usd'] = df.groupby(['region', 'income'])['pvtd_pc_usd'].transform(lambda x: x.fillna(x.mean()))

# Outlier Detection and Handling

# Define a function to remove outliers using the IQR method
def remove_outliers(df, columns):
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

# Remove outliers in key columns
df = remove_outliers(df, ['che', 'gghed', 'pvtd', 'gdp_usd'])

# Encoding categorical variables for modeling
df_encoded = pd.get_dummies(df, columns=['country', 'region', 'income'], drop_first=True)

"""# Exploratory Data Analysis (EDA)

"""

# Distribution of Target Variable (CHE)
plt.figure(figsize=(10, 6))
sns.histplot(df['che'], bins=30, kde=True)
plt.title('Distribution of Current Health Expenditure (CHE)')
plt.xlabel('CHE')
plt.ylabel('Frequency')
plt.show()

# Scatter plot for GDP vs. CHE by Region
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='gdp_usd', y='che', hue='region', palette='Set2')
plt.title('GDP vs CHE by Region')
plt.xlabel('GDP (USD)')
plt.ylabel('CHE')
plt.legend(title='Region')
plt.show()

# Distribution of Government Health Expenditure (GGHEd) by Region
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='region', y='gghed')
plt.title('Distribution of GGHEd by Region')
plt.xlabel('Region')
plt.ylabel('GGHEd')
plt.show()

# Trend Analysis for CHE over Time by Region
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='year', y='che', hue='region')
plt.title('CHE Trends Over Time by Region')
plt.xlabel('Year')
plt.ylabel('CHE')
plt.show()

# Heatmap of Correlation Matrix for Key Financial Metrics
plt.figure(figsize=(12, 8))
correlation_matrix = df[['che', 'gghed', 'pvtd', 'gghed_pc_usd', 'pvtd_pc_usd', 'che_pc_usd', 'oop_pc_usd', 'gdp_usd']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', square=True)
plt.title('Correlation Matrix of Financial Metrics')
plt.show()

# Pairplot for relationships between key financial metrics
sns.pairplot(df[['che', 'gghed', 'pvtd', 'gdp_usd']], diag_kind='kde')
plt.show()

# Boxplot of CHE across different income groups
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='income', y='che', palette='pastel')
plt.title('CHE Distribution by Income Group')
plt.xlabel('Income Group')
plt.ylabel('CHE')
plt.show()

# KDE Plot for distribution of GGHEd across Income Levels
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df, x='gghed', hue='income', fill=True, common_norm=False, palette='viridis')
plt.title('Distribution of GGHEd by Income Level')
plt.xlabel('GGHEd')
plt.ylabel('Density')
plt.show()

# Violin Plot of Private Expenditure (PVTD) by Region
plt.figure(figsize=(10, 6))
sns.violinplot(data=df, x='region', y='pvtd', palette='muted')
plt.title('Distribution of PVTD by Region')
plt.xlabel('Region')
plt.ylabel('PVTD')
plt.show()

# Training the Machine Learning Model

# Define features (X) and target (y)
X = df_encoded.drop(columns=['che', 'year'])
y = df_encoded['che']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.dtypes)

# One-hot encode categorical columns
X_train_encoded = pd.get_dummies(X_train, drop_first=True)
X_test_encoded = pd.get_dummies(X_test, drop_first=True)

# Align columns in case the test set has different dummy columns than the training set
X_test_encoded = X_test_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

"""# Random Forest model"""

# Initialize and train Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_encoded, y_train)

# Calculate scores
train_score = rf_model.score(X_train_encoded, y_train)
test_score = rf_model.score(X_test_encoded, y_test)

print(f'Training R-squared: {train_score}')
print(f'Testing R-squared: {test_score}')

# Import Streamlit library
import streamlit as st

# Streamlit app title
st.title("Healthcare Expenditure Prediction and EDA")

# Sidebar for navigation between EDA and Model Training
section = st.sidebar.selectbox("Choose Section", ["EDA", "Model Training"])

# Streamlit app title
st.title("Healthcare Expenditure Prediction and EDA")

# Sidebar for navigation between EDA and Model Training
section = st.sidebar.selectbox("Choose Section", ["EDA", "Model Training"])

# EDA Section
if section == "EDA":
    st.header("Exploratory Data Analysis (EDA)")

    # Data Preprocessing (Already in your code)
    df = pd.read_excel(file_path)  # Loading the dataset again for preprocessing

    # Data Cleaning and Preprocessing
    df_encoded = pd.get_dummies(df, columns=['country', 'region', 'income'], drop_first=True)

    # Show raw data
    if st.checkbox("Show raw data"):
        st.write(df_encoded.head())

    # Distribution of Target Variable (CHE)
    if st.checkbox("Distribution of Current Health Expenditure (CHE)"):
        fig, ax = plt.subplots()
        sns.histplot(df_encoded['che'], bins=30, kde=True, ax=ax)
        ax.set_title('Distribution of CHE')
        st.pyplot(fig)

    # Scatter plot for GDP vs. CHE by Region
    if st.checkbox("GDP vs CHE by Region"):
        fig, ax = plt.subplots()
        sns.scatterplot(data=df_encoded, x='gdp_usd', y='che', hue='region', palette='Set2', ax=ax)
        ax.set_title('GDP vs CHE by Region')
        st.pyplot(fig)

    # Distribution of Government Health Expenditure (GGHEd) by Region
    if st.checkbox("Distribution of GGHEd by Region"):
        fig, ax = plt.subplots()
        sns.boxplot(data=df_encoded, x='region', y='gghed', ax=ax)
        ax.set_title('GGHEd Distribution by Region')
        st.pyplot(fig)

    # Heatmap of Correlation Matrix for Key Financial Metrics
    if st.checkbox("Correlation Matrix of Financial Metrics"):
        fig, ax = plt.subplots(figsize=(12, 8))
        correlation_matrix = df_encoded[['che', 'gghed', 'pvtd', 'gghed_pc_usd', 'pvtd_pc_usd', 'che_pc_usd', 'oop_pc_usd', 'gdp_usd']].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', square=True, ax=ax)
        ax.set_title('Correlation Matrix of Financial Metrics')
        st.pyplot(fig)

    # Pairplot for relationships between key financial metrics
    if st.checkbox("Pairplot for Relationships"):
        sns.pairplot(df_encoded[['che', 'gghed', 'pvtd', 'gdp_usd']], diag_kind='kde')
        st.pyplot()

# Model Training Section
elif section == "Model Training":
    st.header("Model Training and Prediction")

    # Data Preprocessing (Same as above)
    df = pd.read_excel(file_path)  # Loading the dataset again for preprocessing

    # Data Cleaning and Preprocessing
    df_encoded = pd.get_dummies(df, columns=['country', 'region', 'income'], drop_first=True)

    # Define features (X) and target (y)
    X = df_encoded.drop(columns=['che', 'year'])
    y = df_encoded['che']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest Model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Model evaluation
    train_score = rf_model.score(X_train, y_train)
    test_score = rf_model.score(X_test, y_test)
    st.write(f"Training R-squared: {train_score}")
    st.write(f"Testing R-squared: {test_score}")

    # User input for prediction
    st.subheader("Make a Prediction")
    gdp_usd = st.number_input("GDP (USD)", min_value=0.0, value=1000.0)
    che = st.number_input("Current Health Expenditure (USD)", min_value=0.0, value=500.0)
    gghed = st.number_input("Government Health Expenditure (USD)", min_value=0.0, value=100.0)
    pvtd = st.number_input("Private Expenditure on Health (USD)", min_value=0.0, value=100.0)
    che_pc_usd = st.number_input("Per Capita CHE (USD)", min_value=0.0, value=50.0)
    oop_pc_usd = st.number_input("Per Capita OOP (USD)", min_value=0.0, value=20.0)

    # Prediction Button
    if st.button("Predict CHE"):
        input_data = np.array([[gdp_usd, che, gghed, pvtd, che_pc_usd, oop_pc_usd]])
        prediction = rf_model.predict(input_data)
        st.write(f"Predicted Current Health Expenditure (CHE): {prediction[0]}")
