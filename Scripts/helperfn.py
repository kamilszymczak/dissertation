import pandas as pd
import glob
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def merge_datasets(path):
    """Merging multiply csv datasets into one DataFrame

    :param folder_path: Relative path of folder containing all datasets 
    :type folder_path: string
    :return: Single DataFrame of all datasets
    :rtype: pandas.dataframe
    """
    # path = r'E:\GitHubProjects\dissertation\scraper\approved_datasets'
    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    return pd.concat(li, axis=0, ignore_index=True)

def get_data(df):
    return df['review'], df['score']


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


def remove_punctuations(token):
    return [re.sub(r'(\[+|]+|\!+|"+|\$+|%+|&+|\'+|\(+|\)+|\*+|\++|,+|\.+|:+|;+|=+|#+|@+|\?+|\[+|\^+|_+|`+|{+|\|+|\}+|~+|-+|]+)\1+', r'\1', string) for string in token]

#lower case tokens
def lower_token(token): 
    return [w.lower() for w in token]  

def remove_mentions(texts):
    return [re.sub(r"(?:\@|https?\://)\S+", "", text) for text in texts]

def remove_stopwords(text):
    return [item for item in text if item not in stop_words()]

def remove_uni_names(text):
    return [item for item in text if item not in uni_names()]

lemmatizer = WordNetLemmatizer()
def lemmatization(text):
    return [lemmatizer.lemmatize(item) for item in text]

def balance_dataset(df):
    # Shuffle the dataset
    shuffled_df = df.sample(frac=1, random_state=14)

    # Put all negative reviews/class in a separate dataset.
    negative_df = shuffled_df.loc[shuffled_df['score'] == 0]

    #Randomly select negative_df size postive reviews (majority class)
    positive_df = shuffled_df.loc[shuffled_df['score'] == 1].sample(n=negative_df.shape[0])

    # Concatenate both dataframes again
    return pd.concat([negative_df, positive_df])
