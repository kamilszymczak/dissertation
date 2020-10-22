import requests
from bs4 import BeautifulSoup
import pandas as pd


urls = ['https://www.studentcrowd.com/university-l1006588-s1008458-university_of_stirling-stirling']

def score_conversion(score):
    score = int(score)
    if score <= 2:
        return 0
    if score > 3:
        return 1
    return 2


def build_dataset(seed_url):
    reviews_data = []
    
    for url in urls:

        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')

        reviews = [
            {'review': review.find('span', attrs={"itemprop": "reviewBody"}).string , 'score': score_conversion(str(review.find('div', {"class": "review-box__stars"}))[-9:-8])}

            for review in soup.find_all('div', attrs={"itemprop": "review"})]   

    
        reviews_data.extend(reviews)

    return reviews_data


dataset = build_dataset(urls)

print(dataset)

df =  pd.DataFrame(dataset)
df = df[['review', 'score']]

df.to_csv (r'C:\Users\Kamcio\Desktop\export_dataframe.csv', index = False, header=True)