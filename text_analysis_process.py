import pandas as pd
import ast
import re

from lib.text_analysis_function import clean_text, detect_lang, pourcentageResult
from lib.text_analysis_function import english_SIA_textAnalysis, french_SIA_textAnalysis
#from text_analysis_function import french_TextBlob_textAnalysis, english_TextBlob_textAnalysis, duplicate_coms_by_likes

"""
ANALYSE PROCESS WITH PERCENTAGE RESULT POS/NEG/NEU
"""

def sentiment_video(num_video, yt_comment):
    list_positive, list_negative, list_neutral = [], [], []
    for i in range(num_video):
        try :
            row1 = yt_comment.iloc[[i]]
            coms = row1['comment_list'].tolist()
            com_list = ast.literal_eval(coms[0])
        
            if com_list == []:
                a = 1/0

            data_text = pd.DataFrame(com_list)

            # Clean Text
            data_text['comment'] = data_text['comment'].apply(clean_text)
            remove_special_char = lambda x: re.sub("[$&+:;=@#|_<>.^*()%-]"," ",x)
            data_text['comment']= data_text['comment'].apply(remove_special_char)

            # Detect language
            data_text['lang'] = list(map(detect_lang, data_text['comment']))

            # Text Analysis (2 possible model) 
            data_text['result'] = [french_SIA_textAnalysis(x) if (y == 'fr') 
                else english_SIA_textAnalysis(x)  for x,y in zip(data_text['comment'], data_text['lang'])]
            
            #data_text['result'] = [french_TextBlob_textAnalysis(x) if (y == 'fr') 
                #else english_TextBlob_textAnalysis(x) for x,y in zip(data_text['comment'], data_text['lang'])]

            # Delete comment post after video be in trending list
            trend_date = row1['trending_date'].tolist()
            data_result = data_text[data_text['date'] <= trend_date[0]]
            data_result = data_result.reset_index(drop=True)

            # Duplique les commentaires en fonction de leur like
            #result_duplicate = duplicate_coms_by_likes(data_result['likes'], data_result['result'])
            #positive, negative, neutral = pourcentageResult(result_duplicate)

            positive, negative, neutral = pourcentageResult(data_text['result'])

            list_positive.append(positive)
            list_negative.append(negative)
            list_neutral.append(neutral)
        except:
            list_positive.append(None)
            list_negative.append(None)
            list_neutral.append(None)
            continue

    df = yt_comment.iloc[:num_video, 0:16]
    df['positive'] = list_positive
    df['negative'] = list_negative
    df['neutral'] = list_neutral
    return df
