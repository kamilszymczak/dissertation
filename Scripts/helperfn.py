import pandas as pd
import glob
import re


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


def remove_punctuations(string):
    return re.sub('\!\!+', '!', string)

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