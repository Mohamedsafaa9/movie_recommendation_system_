# -*- coding: utf-8 -*-
"""Movie Recommendation System .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bQXsCKacB-SPOPogkvu3qduE2bPCzGrL
"""

!kaggle datasets download -d tmdb/tmdb-movie-metadata
!kaggle datasets download -d rounakbanik/the-movies-dataset

! unzip  tmdb-movie-metadata.zip
! unzip  the-movies-dataset.zip

import pandas as pd
import numpy as np
df1=pd.read_csv('tmdb_5000_credits.csv')
df2=pd.read_csv('tmdb_5000_movies.csv')
# Display the first few rows of each dataset
print("Credits DataFrame:")
print(df1.head())

print("\nMovies DataFrame:")
print(df2.head())

# Rename 'id' column in df2 to 'movie_id' to match df1
df2.rename(columns={'id': 'movie_id'}, inplace=True)

# Merge the datasets on 'movie_id'
merged_df = pd.merge(df1, df2, on='movie_id')

# Display the first few rows of the merged DataFrame
print("\nMerged DataFrame:")
print(merged_df.head())

"""a-  Summary Statistics"""

print("\nMerged DataFrame Info:")
print(merged_df.info())

# Summary statistics of the numerical columns
print("\nSummary Statistics:")
print(merged_df.describe())

"""b. Movie Popularity Analysis

"""

import matplotlib.pyplot as plt

# Plot the distribution of movie popularity
plt.figure(figsize=(10, 6))
plt.hist(merged_df['popularity'].dropna(), bins=50, color='blue', edgecolor='black')
plt.title('Distribution of Movie Popularity')
plt.xlabel('Popularity')
plt.ylabel('Frequency')
plt.show()

"""c. Top Movies by Revenue

"""

# Sort by revenue and select top 10 movies
top_revenue_movies = merged_df[['title_x', 'revenue']].sort_values(by='revenue', ascending=False).head(10)

print("\nTop 10 Movies by Revenue:")
print(top_revenue_movies)

print(merged_df.columns)

"""d. Movies with Highest Vote Average

"""

# Sort by vote average and select top 10 movies
top_voted_movies = merged_df[['title_x', 'vote_average']].sort_values(by='vote_average', ascending=False).head(10)

print("\nTop 10 Movies by Vote Average:")
print(top_voted_movies)

"""e. Genre Analysis

"""

# Count the number of movies in each genre
# Assuming genre column contains comma-separated genres
genre_counts = merged_df['genres'].str.split(',', expand=True).stack().value_counts()

print("\nGenre Distribution:")
print(genre_counts)

"""Analyze Trends Over Time"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Convert release_date to datetime
merged_df['release_date'] = pd.to_datetime(merged_df['release_date'], errors='coerce')

# Extract the year
merged_df['release_year'] = merged_df['release_date'].dt.year

# Group by year and calculate the mean for relevant features
yearly_trends = merged_df.groupby('release_year').agg({'revenue': 'mean', 'budget': 'mean', 'popularity': 'mean'}).reset_index()

# Plot trends over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=yearly_trends, x='release_year', y='revenue', label='Average Revenue')
sns.lineplot(data=yearly_trends, x='release_year', y='budget', label='Average Budget')
sns.lineplot(data=yearly_trends, x='release_year', y='popularity', label='Average Popularity')
plt.title('Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Values')
plt.legend()
plt.show()

"""Compare Production Companies"""

from ast import literal_eval

# Convert the 'production_companies' from string to a list
merged_df['production_companies'] = merged_df['production_companies'].apply(lambda x: literal_eval(x) if pd.notna(x) else [])

# Flatten the production companies list
company_revenue = {}
for index, row in merged_df.iterrows():
    for company in row['production_companies']:
        name = company['name']
        if name in company_revenue:
            company_revenue[name]['revenue'].append(row['revenue'])
        else:
            company_revenue[name] = {'revenue': [row['revenue']]}

# Calculate average revenue per company
company_avg_revenue = {k: sum(v['revenue']) / len(v['revenue']) for k, v in company_revenue.items() if len(v['revenue']) > 0}

# Convert to DataFrame
company_df = pd.DataFrame.from_dict(company_avg_revenue, orient='index', columns=['average_revenue']).reset_index()
company_df.rename(columns={'index': 'production_company'}, inplace=True)

# Top 10 production companies by average revenue
top_companies = company_df.sort_values(by='average_revenue', ascending=False).head(10)

# Plot top companies by average revenue
plt.figure(figsize=(10, 6))
sns.barplot(data=top_companies, x='average_revenue', y='production_company', palette='viridis')
plt.title('Top 10 Production Companies by Average Revenue')
plt.xlabel('Average Revenue')
plt.ylabel('Production Company')
plt.show()

"""Analysis of Cast and Crew"""

from ast import literal_eval

# Convert 'cast' and 'crew' from string to list, handling potential errors
merged_df['cast'] = merged_df['cast'].apply(lambda x: literal_eval(x) if isinstance(x, str) and pd.notna(x) else [])
merged_df['crew'] = merged_df['crew'].apply(lambda x: literal_eval(x) if isinstance(x, str) and pd.notna(x) else [])


# Extract top actors, directors, and writers
actors = []
directors = []
writers = []

for index, row in merged_df.iterrows():
    for person in row['cast']:
        actors.append(person['name'])
    for person in row['crew']:
        if person['job'] == 'Director':
            directors.append(person['name'])
        elif person['job'] == 'Writer':
            writers.append(person['name'])

# Convert to DataFrame and calculate popularity and revenue
actors_df = pd.DataFrame(actors, columns=['actor'])
actors_df['revenue'] = merged_df['revenue'].repeat(merged_df['cast'].str.len()).reset_index(drop=True)
actors_df['popularity'] = merged_df['popularity'].repeat(merged_df['cast'].str.len()).reset_index(drop=True)

directors_df = pd.DataFrame(directors, columns=['director'])
# Calculate the number of directors for each movie and repeat revenue and popularity accordingly
director_counts = merged_df['crew'].apply(lambda x: len([person for person in x if person['job'] == 'Director']))
directors_df['revenue'] = merged_df['revenue'].repeat(director_counts).reset_index(drop=True)
directors_df['popularity'] = merged_df['popularity'].repeat(director_counts).reset_index(drop=True)

# Plot top 10 actors by average revenue
top_actors = actors_df.groupby('actor').mean().sort_values(by='revenue', ascending=False).head(10).reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(data=top_actors, x='revenue', y='actor', palette='viridis')
plt.title('Top 10 Actors by Average Movie Revenue')
plt.xlabel('Average Revenue')
plt.ylabel('Actor')
plt.show()

# Convert 'release_date' to datetime
merged_df['release_date'] = pd.to_datetime(merged_df['release_date'], errors='coerce')

# Extract year from 'release_date'
merged_df['release_year'] = merged_df['release_date'].dt.year

# Plot number of movies released per year
movies_per_year = merged_df['release_year'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x=movies_per_year.index, y=movies_per_year.values)
plt.title('Number of Movies Released Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Movies')
plt.show()

# Plot average revenue and popularity per year
avg_stats_per_year = merged_df.groupby('release_year').agg({'revenue': 'mean', 'popularity': 'mean'}).reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=avg_stats_per_year, x='release_year', y='revenue', label='Average Revenue')
sns.lineplot(data=avg_stats_per_year, x='release_year', y='popularity', label='Average Popularity')
plt.title('Average Revenue and Popularity of Movies Over Time')
plt.xlabel('Year')
plt.ylabel('Average Value')
plt.legend()
plt.show()

"""Visualize Relationships Between Different Features



"""

# Scatter plot for budget vs. revenue
plt.figure(figsize=(10, 6))
sns.scatterplot(data=merged_df, x='budget', y='revenue', alpha=0.6)
plt.title('Budget vs. Revenue')
plt.xlabel('Budget')
plt.ylabel('Revenue')
plt.show()

# Correlation matrix to find correlated features
correlation_matrix = merged_df[['budget', 'revenue', 'popularity', 'runtime', 'vote_average']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Movie Features')
plt.show()

# Pair plot to visualize relationships between multiple features
sns.pairplot(merged_df[['budget', 'revenue', 'popularity', 'runtime', 'vote_average']], diag_kind='kde')
plt.show()

"""Insights on Data Distribution and Feature Importance"""

# Visualize the distribution of key features
plt.figure(figsize=(10, 6))
sns.histplot(merged_df['revenue'], kde=True, bins=30)
plt.title('Distribution of Movie Revenue')
plt.xlabel('Revenue')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(merged_df['vote_average'], kde=True, bins=30)
plt.title('Distribution of Movie Ratings')
plt.xlabel('Vote Average')
plt.show()

# Feature importance using correlation with revenue
important_features = correlation_matrix['revenue'].sort_values(ascending=False)
print('Feature Importance based on correlation with revenue:')
print(important_features)

"""Explore Genre Popularity and Performance

"""

# Plot average revenue and popularity by genre
plt.figure(figsize=(12, 6))
sns.barplot(data=genre_stats, x='revenue', y='genre', palette='coolwarm')
plt.title('Average Revenue by Genre')
plt.xlabel('Average Revenue')
plt.ylabel('Genre')
plt.show()

# Plot average popularity by genre

plt.figure(figsize=(12, 6))
sns.barplot(data=genre_stats, x='popularity', y='genre', palette='viridis')
plt.title('Average Popularity by Genre')
plt.xlabel('Average Popularity')
plt.ylabel('Genre')
plt.show()

!pip install pycaret

!pip install --upgrade scipy

import pandas as pd

# Load the datasets
df1 = pd.read_csv('tmdb_5000_credits.csv')
df2 = pd.read_csv('tmdb_5000_movies.csv')

# Rename 'id' column in df2 to 'movie_id' to match df1
df2.rename(columns={'id': 'movie_id'}, inplace=True)

# Merge the datasets on 'movie_id'
merged_df = pd.merge(df1, df2, on='movie_id')

# Drop unnecessary columns and handle missing values
# Here, we will focus on predicting 'revenue' and using a subset of columns for simplicity
data = merged_df[['budget', 'popularity', 'runtime', 'vote_average', 'revenue']].dropna()

from pycaret.regression import *

# Initialize the PyCaret setup
regression_setup = setup(data=data, target='revenue', session_id=123)

# Compare different regression models
best_model = compare_models()

# Create a specific regression model (e.g., Random Forest)
rf_model = create_model('rf')

# Evaluate the model
evaluate_model(rf_model)

# Finalize the model
final_model = finalize_model(rf_model)

# Save the model
save_model(final_model, 'final_movie_revenue_model')

# Load the saved model
loaded_model = load_model('final_movie_revenue_model')

# Make predictions on new data
predictions = predict_model(loaded_model, data=data)

print(predictions.head())

# Plot feature importance
plot_model(final_model, plot='feature')