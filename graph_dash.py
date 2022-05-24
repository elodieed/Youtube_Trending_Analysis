import pandas as pd
from functools import reduce

from lib.function_test import get_nameCategory, get_monthNyears

def get_tag(liste):
    liste = liste.split('|')
    return liste 

def all_tags(yt_comment):
    l , datT, cat  = [], [], []
    for i in range(len(yt_comment['tags'])):
        tags = get_tag(yt_comment['tags'][i])
        l += tags
        datT += list(map(lambda x: yt_comment['trending_date'][i], tags))
        cat += list(map(lambda x: yt_comment['categoryId'][i], tags))

    data_tags = pd.DataFrame()
    data_tags['tags'] = l
    data_tags['date'] = datT
    data_tags['category'] = cat
    return data_tags

def occurance_tags(data_tags):
    data = pd.DataFrame()
    tags_list = list(set(data_tags['tags']))
    data['tags'] = tags_list
    data['occurance'] = [list(data_tags['tags']).count(j) for j in tags_list]
    return data

#----------------------------------------------------------------------------

def view_evolution(yt_comment):
    yt_comment['publishedAt'] = yt_comment['publishedAt'].apply(lambda x: get_monthNyears(x))

    df_monthCategory = yt_comment.groupby(['categoryId', 'publishedAt'])['view_count'].sum()
    df_monthCategory = df_monthCategory.reset_index()
    return df_monthCategory

#--------------------------------------------------------------------------

def repartion_video_Category(yt_comment):
    list_categorie = list(yt_comment['categoryId'])
    categorie = list(set(yt_comment['categoryId']))

    nbr_video = [list_categorie.count(j) for j in categorie]

    total = int(reduce(lambda x, y : x+y, nbr_video))
    pourcentage = list(map(lambda x : round(x*100/total, 2), nbr_video))

    df_pro = pd.DataFrame()
    df_pro['Category'] = categorie
    df_pro['Video %'] = pourcentage
    return df_pro

#--------------------------------------------------------------------------
data_path = './Data/FR_youtube_trending_data.csv'
yt_comment = pd.read_csv(data_path)

yt_comment['categoryId'] = yt_comment['categoryId'].apply(lambda x: get_nameCategory(int(x)))



