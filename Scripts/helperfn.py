import pandas as pd
import glob
import re
from nltk.corpus import stopwords

def merge_datasets(folder_path):
    """Merging multiply csv datasets into one DataFrame

    :param folder_path: Relative path of folder containing all datasets 
    :type folder_path: string
    :return: Single DataFrame of all datasets
    :rtype: pandas.dataframe
    """
    path = r'E:\GitHubProjects\dissertation\scraper\approved_datasets'
    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    return pd.concat(li, axis=0, ignore_index=True)

def get_data(df):
    return df['review'], df['score']


def remove_punctuations(token):
    return [re.sub(r'(\[+|]+|\!+|"+|\$+|%+|&+|\'+|\(+|\)+|\*+|\++|,+|\.+|:+|;+|=+|#+|@+|\?+|\[+|\^+|_+|`+|{+|\|+|\}+|~+|-+|]+)\1+', r'\1', string) for string in token]

#lower case tokens
def lower_token(token): 
    return [w.lower() for w in token]  

def vectorize(review):
    for word in review:
        if word in vocab:
            vectors.append(model[word])
        else:
            pass
            #word not in pre-trained ebeddings


import matplotlib.pyplot as plt
import seaborn as sns

def balance_dataset(df):
    # Shuffle the dataset
    shuffled_df = df.sample(frac=1, random_state=14)

    # Put all negative reviews/class in a separate dataset.
    negative_df = shuffled_df.loc[shuffled_df['score'] == 0]

    #Randomly select 108 postive reviews (majority class), as there are 108 negative reviews
    positive_df = shuffled_df.loc[shuffled_df['score'] == 1].sample(n=negative_df.shape[0])

    # Concatenate both dataframes again
    return pd.concat([negative_df, positive_df])


def stop_words():
    stop = stopwords.words('english')
    #convert to set for faster retrival
    stop = set(stop)
    stop_to_remove = {'no', 'nor', 'not', 'very', 'don', "don't", "aren't", 'couldn', "couldn't", 'didn', "didn't",
        'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
        'isn', "isn't", 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
        'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}

    #remove negations as stopwords as they provide valauble meaning and should not be removed
    return stop.difference(stop_to_remove)

def uni_names():
    return {'anglia', 'ruskin', 'birmingham', 'brunel', 'buckinghamshire', 'cardiff', 'metropolitan',
    'napier', 'heriot', 'watt', 'kingston', 'liverpool', 'metropolitan', 'south', 'middlesex', 'oxford',
    'brookes', 'teesside', 'westminster', 'wolverhampton', 'suffolk', 'ltd', 'london', 'aberdeen',
    'abertay', 'dundee', 'bedfordshire', 'cumbria', 'derby', 'east london', 'edinburgh', 'glasgow',
    'northampton', 'salford', 'south', 'wales', 'stirling', 'strathclyde', 'sunderland', 'west', 'scotland', 'ulster', 'worcester'}