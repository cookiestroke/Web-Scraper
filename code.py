import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
titles = []
categories = []
tags = []
replies = []
posts = []
comments = []
# You can add categories manually as we are already sorting by categories
cats = 'Get Help,Git'
# Find the number of pages in categories to determine the range
for i in range(0, 15):
    # Add the URL to the category page you have to scrape
    URL = 'https://discuss.codecademy.com/c/get-help/git/1813'+'?page='+str(i)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_='topic-list-item')
    for result in results:
        topic = result.find('a', class_='title')
        url1 = topic['href']
        page1 = requests.get(url1)
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        result1 = soup1.find_all(class_='post')
        comment = ''
        for i in result1[1:]:
            comment += i.text
        tagg = result.find_all('a', class_='discourse-tag')
        tagss = ''
        for t in tagg:
            tagss += t.text+','
        tagss = tagss.rstrip(',')
        reps = result.find('td', class_='replies')
        titles.append(topic.text)
        categories.append(cats)
        tags.append(tagss)
        replies.append(reps.span.text)
        posts.append(result1[0].text)
        comments.append(comment)
    # To prevent DDoS
    time.sleep(3)

getcsv = pd.DataFrame({'Title': titles,
                       'Categories': categories,
                       'Tags': tags,
                       'Replies': replies,
                       'Post': posts,
                       'Comment': comments,
                       })

print(getcsv.info())

getcsv.to_csv('output.csv')
