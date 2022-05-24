from langdetect import detect
import emoji

import nltk
nltk.download('vader_lexicon')

from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer as SIA

"""
TRAITEMENT DU TEXT
"""
def clean_text(text):
    text = str(text)
    text = text.replace('<br>', ' ').replace('<b>', ' ').replace('</b>', '')
    text = text.replace('&quot;', '').replace('\xa0', '').replace("&#39;", "'" )
    text = text.replace('\r', '')
    text = text.replace('<a href="https://www.youtube.com/watch?', '').replace('</a>', ' ')
    text = emoji.demojize(text)
    return text

"""
DETECTION DE LA LANGUE
"""
def detect_lang(text):
    try:
        lang = detect(text) 
    except:
        lang = '?'
    return lang

"""
ANALYSE SENTIMENT FRANCAIS / ANGLAIS
"""
def french_TextBlob_textAnalysis(commentVideo): 
    analysis = TextBlob(commentVideo,pos_tagger=PatternTagger(),analyzer=PatternAnalyzer())
    score = analysis.sentiment[0]
    if score < 0:
        result = -1
    elif score > 0:
        result = 1
    else :   
        result = 0
    return result

def french_SIA_textAnalysis(commentVideo):
    score = SIA().polarity_scores(commentVideo)
    neg = score['neg']
    pos = score['pos']
    if neg > pos:
        result = -1
    elif pos > neg:
        result = 1
    elif pos == neg:   
        result = 0
    return result

def english_TextBlob_textAnalysis(commentVideo): 
    analysis = TextBlob(commentVideo)
    score = analysis.sentiment[0]
    if score < 0:
        result = -1
    elif score > 0:
        result = 1
    else :   
        result = 0
    return result

def english_SIA_textAnalysis(commentVideo):
    score = SentimentIntensityAnalyzer().polarity_scores(commentVideo)
    neg = score['neg']
    pos = score['pos']
    if neg > pos:
        result = -1
    elif pos > neg:
        result = 1
    elif pos == neg:   
        result = 0
    return result

"""
RESULTAT POURCENTAGE
"""
def percentage(part,whole):
    return round(100 * float(part)/float(whole), 2) 

def pourcentageResult(yt_comment):
    numOfComment = len(yt_comment)
    positive = len(list(filter(lambda x : x==1, yt_comment)))
    negative = len(list(filter(lambda x : x==-1, yt_comment)))
    neutral = len(list(filter(lambda x : x==0, yt_comment)))
    
    positive = percentage(positive, numOfComment)
    negative = percentage(negative, numOfComment)
    neutral = percentage(neutral, numOfComment)
    
    return positive, negative, neutral

"""
DUPLIQUE LES COMMENTAIRES EN FONCTION DE LEUR NOMBRE DE LIKE
"""

def add_point_to_coms(likes, result, liste_result):
    crea_list = list(range(likes))
    liste_result += list(map(lambda x : result, crea_list))
    return liste_result

def duplicate_coms_by_likes(list_likes, list_result):
    result = []
    for i in range(len(list_likes)):
        if list_result[i] != 0:
            coms_by_likes = add_point_to_coms(list_likes[i], list_result[i], result)
        else:
            continue

    result = list(list_result)
    result += coms_by_likes
    return result