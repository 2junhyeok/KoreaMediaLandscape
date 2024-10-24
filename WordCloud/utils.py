import pandas as pd
import numpy as np
import os
import re
import copy
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords



# Kiwi 초기화
kiwi = Kiwi(typos='basic')
stopwords = Stopwords() # 스탑워드

def get_source_type(source, 보수, 진보, 기타): # source가 보수면 0, 진보면 1, 기타면 2, 예외처리 -1
    if source in 보수:
        return 0
    elif source in 진보:
        return 1
    elif source in 기타:
        return 2
    else:
        return -1  

def remove_bracketed_text_and_media(title, media_list): # 괄호 안의 텍스트 제거 및 신문이름 제거
    title = re.sub(r'\[.*?\]', '', title).strip() # 대괄호 텍스트 제거
    for media in media_list:
        title = title.replace(media, '').strip() # 신문사 이름 제거
    return title

# def add_stopword(stopwords_list, stopwords = stopwords):
#     for word in stopwords_list:
#         stopwords.add(word)
# 추가적인 스탑워드 적용하는 용도


def preprocess_korean(text, stopwords=None): # 교수님 제공 전처리 파일
    my_text = copy.copy(text)
    my_text = my_text.replace('\n', ' ')
    my_text = kiwi.space(my_text)
    sents = kiwi.split_into_sents(my_text)
    p = re.compile('[^ㄱ-ㅎㅏ-ㅣ가-힣 ]')
    all_result = []
    
    for sent in sents:
        token_result = kiwi.tokenize(sent.text, stopwords=stopwords)
        token_result = kiwi.join(token_result)
        token_result = p.sub(' ', token_result)
        # 단어 개수가 1개 이상인 경우에만 추가
        if len(token_result.split()) > 1:
            all_result.append(token_result)
            
    all_result = ' '.join(all_result)
    return all_result

def sep_data(data, col_name = 'source_type', sep = int): # source_type의 값에 해당하는 dataframe만 생성
    return data[data[col_name] == sep].reset_index(drop = True)

def preprocess_sep_data(data): # 전처리 함수
    df_list = []
    for i in range(0,3): # 보수, 진보, 기타 하나씩 전처리를 해서 리스트에 추가
        df = sep_data(data = data, sep = i)
        # preprocessed_Title 열을 생성
        df['preprocessed_Title'] = df['Title'].apply(lambda x : preprocess_korean(x, stopwords=stopwords))
        df_list.append(df)
    return df_list

def combine_all_data(df_list): # 분리된 데이터를 하나로 합치는 함수
    all_data_list = []
    for df in df_list: # 각 보수, 진보, 기타 df_list를 하나씩 받아서
        all_text = ' '.join(df['preprocessed_Title']) # 해당 열의 전처리된 제목을 모두 join
        all_data_list.append(all_text) # join된 보수, 진보, 기타 언론사의 전처리 제목 문자열을 빈 리스트에 추가
    return all_data_list

def load_all_csv_files(directory='data'): # 해당 디렉토리의 csv파일을 불러오는 함수
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    return csv_files


def remove_keyword(title, keyword): # 제목에 해당 키워드가 있다면 제거하는 함수
    title = title.replace(keyword, '').strip()
    return title