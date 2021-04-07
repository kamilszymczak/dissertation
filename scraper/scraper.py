import requests
from bs4 import BeautifulSoup
import pandas as pd

def score_conversion(score):
    score = int(score)
    if score <= 2:
        return 0
    if score > 3:
        return 1
    return 2

def build_dataset(seed_url, separateFile=True):
    reviews_data = []

    for url in urls:
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')

        reviews = [
            {'review': review.find('span', attrs={"itemprop": "reviewBody"}).string , 'score': score_conversion(str(review.find('div', {"class": "review-box__stars"}))[-9:-8])}
            for review in soup.find_all('div', attrs={"itemprop": "review"})]   

        if separateFile:
            #Making file name from studetcrowd url
            dataset_name = url.split("-")
            dataset_name = dataset_name[-2]
            toCSV(reviews, dataset_name)

        reviews_data.extend(reviews)
    return reviews_data

def toCSV(dataset, filename='export_dataframe'):
    df =  pd.DataFrame(dataset)
    df = df[['review', 'score']]
    df.to_csv (filename + '.csv', index = False, header=True, encoding='utf-8-sig')

urls = ['https://www.studentcrowd.com/university-l1002555-s1008268-heriot_watt_university-edinburgh']
dataset = build_dataset(urls)

print("Export Completed!")