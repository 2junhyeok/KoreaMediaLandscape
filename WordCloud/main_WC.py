# kiwi 가상환경
import pandas as pd
from wordcloud import WordCloud
import numpy as np
from utils import *
import config
from kiwipiepy.utils import Stopwords



def main():
    # 설정 불러오기
    font_path = config.font_path # config의 폰트경로
    pattern = config.pattern # config의 키워드 패턴

    보수 = config.보수 # 키워드에서의 보수 언론사
    진보 = config.진보 # 키워드에서의 진보 언론사
    기타 = config.기타 # 키워드에서의 기타 언론사
    all_media = config.all_media # 네이버뉴스 우측에 모여있는 언론사들

    
    
    for file_path in load_all_csv_files(): # csv파일을 하나씩 다 불러와서 반복문을 진행
        file_path = f'data/{file_path}' # 파일 경로를 변수에 저장
        
        keyword = re.search(pattern, file_path).group(0) # file_path에서 keyword 뽑기
        # 데이터 불러오기
        data = pd.read_csv(file_path)
        
        # 데이터 전처리
        data.drop_duplicates(subset=['Title'], inplace=True) # 중복된 제목 삭제
        data['Title'] = data['Title'].apply(remove_bracketed_text_and_media, media_list=all_media) # 언론사 명 삭제
        data['Title'] = data['Title'].apply(remove_keyword, keyword = keyword) # 키워드 제거
        data['Title'] = data['Title'].str.replace('^ +', "") # 선행하는 공백을 제거
        data['Title'].replace('', np.nan, inplace=True) # 제목이 공백이면 nan으로 채움
        data = data.dropna(how='any').reset_index(drop=True) # nan으로 되어있는 뉴스기사는 drop
        
        # 소스 타입 열을 추가(언론 성향에 대한 class)
        data['source_type'] = data['Source'].apply(lambda x: get_source_type(x, 보수, 진보, 기타))
        
        # 데이터 전처리 및 분류
        df_list = preprocess_sep_data(data)
        
        # 모든 텍스트 결합
        all_texts = combine_all_data(df_list)
        
        # 워드 클라우드 생성 및 저장
        cloud = WordCloud(font_path=font_path, background_color='white', width=800, height=800)
        
        for idx, text in enumerate(all_texts): # 보수, 진보, 기타 순으로 워드클라우드를 반복문으로 생성 및 저장
            cloud.generate(text)
            cloud.to_file(f'WordCloud/wordcloud_{idx}_{keyword}.png')

if __name__ == '__main__':
    main()# data 폴더의 모든 csv 파일에 대해 워드클라우드 적용