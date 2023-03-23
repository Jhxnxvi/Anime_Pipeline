# Importing libraries for data analysis
import pandas as pd
import requests
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import boto3

# Step 1: Extracting data from the external source 
# Then, it defines the URL of the website to be scraped, and it sends an HTTP request to retrieve the content of the webpage. 
top_anime_url = 'https://myanimelist.net/topanime.php' + '/topanime.php'
response = requests.get(top_anime_url)

# Checking if the request was successful using status_code attribute of the response object.
if response.status_code != 200:
    print("Error: Unable to retrieve data")
else:
# Step 2: Transforming the data
# If the request is successful, it proceeds to extract the required information from the HTML content using the BeautifulSoup library.    
# The code finds the table header and rows containing the anime information and extracts the required information such as rank, title, rating, image URL, episodes, and dates.
    doc = BeautifulSoup(response.text, 'html.parser')
    headers = doc.find('tr', class_ = 'table-header').find_all('td')
    row_content = doc.find_all('tr', {'class' : "ranking-list"})
# A custom function named parse_episodes is defined to parse the episode information from the HTML content.
    def parse_episodes(listt):
        result = []
        for i in listt[:2]:
            r = i.strip()
            result.append(r)
        return result

    top_anime = []
    for row in row_content:
        episode = parse_episodes(row.find('div', class_ = "information di-ib mt4").text.strip().split('\n'))
        ranking = {
            'Rank' : row.find('td', class_ = "rank ac").find('span').text,
            'Title': row.find('div', class_="di-ib clearfix").find('a').text,
            'Rating': row.find('td', class_="score ac fs14").find('span').text,
            'Image_URL': row.find('td', class_ ='title al va-t word-break').find('img')['data-src'],
            'Episodes': episode[0],
            'Dates': episode[1]
        }
        top_anime.append(ranking)

# Create a pandas DataFrame from the top_anime list
df = pd.DataFrame(top_anime)

# Save the DataFrame as a CSV file
df.to_csv('top_anime.csv', index=False)


 # Step 3: Creating visualizations
# First, we'll create a scatter plot using Seaborn to show the relationship between the rank and rating of the top anime.
df = pd.DataFrame(top_anime)
sns.scatterplot(x='Rank', y='Title', data=df)
plt.title('Rating of Top Anime')
plt.show()
    
 # Next, we'll create a bar chart using Seaborn to show the top 10 anime based on rating.
top10 = df.sort_values('Rating', ascending=False).head(10)
sns.barplot(x='Title', y='Rating', data=top10)
plt.xticks(rotation=90)
plt.title('Top 10 Anime based on Rating')
plt.show()
    
s3 = boto3.resource('s3', 
aws_access_key_id='AKIAUJ2ZHVF3HLVOUDVO',
aws_secret_access_key='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'
)

bucket_name = 'xanderproject'
file_name = 'top_anime.csv'

s3.Object(bucket_name, file_name).put(Body=df.to_csv(index=False))