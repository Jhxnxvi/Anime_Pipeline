import pandas as pd

# Read the data from the CSV files
anime_df = pd.read_csv('top_anime.csv')
manga_df = pd.read_csv('top_manga.csv')

# Merge the dataframes based on the title column
merged_df = pd.merge(anime_df, manga_df, on='Title', how='inner')

# Save the merged dataframe to a new CSV file
merged_df.to_csv('anime_manga_comparison.csv', index=False)

