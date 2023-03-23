# Importing libraries for data analysis
import pandas as pd
import requests
from bs4 import BeautifulSoup 
import seaborn as sns
import matplotlib.pyplot as plt
import boto3


# Step 1: Extracting data from the external source 
# Then, it defines the URL of the website to be scraped, and it sends an HTTP request to retrieve the content of the webpage. 
top_manga_url = "https://myanimelist.net/topmanga.php"
response = requests.get(top_manga_url)

# Checking if the request was successful using status_code attribute of the response object.
if response.status_code != 200:
    print("Error: Unable to retrieve data")
else:
# Step 2: Transforming the data
# If the request is successful, it proceeds to extract the required information from the HTML content using the BeautifulSoup library.    
# The code finds the table header and rows containing the anime information and extracts the required information such as rank, title, image URL, score, and manga url.
    doc = BeautifulSoup(response.text, 'html.parser')
    doc = BeautifulSoup(response.text, 'html.parser')
    headers = doc.find('tr', class_ = 'table-header').find_all('td')
    rows = doc.find_all('tr', {'class' : "ranking-list"})

top_manga = []

for row in rows[1:]:
    rank = row.find("td", class_="rank").text.strip()
    title = row.find("h3", class_="manga_h3").find("a").text.strip()
    score = row.find("td", class_="score").text.strip()
    manga_url = row.find("td", class_="title al va-t clearfix word-break").find("a")["href"]
    manga_img_url = row.find("td", class_="title al va-t clearfix word-break").find("img")["data-src"]

    top_manga.append({"Rank": rank, "Title": title, "Score": score, "URL": manga_url, "Image_URL": manga_img_url})
    
# Creating a pandas DataFrame from the top_manga list
df = pd.DataFrame(top_manga)

# Saving the DataFrame as a CSV file
df.to_csv('top_manga.csv', index=False)

    
# Step 3: Creating visualizations
# First, we'll create a scatter plot using Seaborn to show the relationship between the rank and rating of the top anime.
df = pd.DataFrame(top_manga)
sns.scatterplot(x='Rank', y='Title', data=df)
plt.title('Rating of Top Mangas')
plt.show()
    
 # Next, we'll create a bar chart using Seaborn to show the top 10 manga based on rating.
top10 = df.sort_values('Rating', ascending=False).head(10)
sns.barplot(x='Title', y='Rank', data=top10)
plt.xticks(rotation=90)
plt.title('Top 10 Mangas based on Rating')
plt.show()




