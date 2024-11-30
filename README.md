본 프로젝트는 **'2024-1 텍스트데이터분석 수업'** 에서 진행한 프로젝트입니다.

<br/>

## 👬 팀원
- 이준혁, 조현식

## 🕓 기간
- 24.04.27 ~ 24.06.02

## 📑 주제
- 뉴스 제목으로 확인하는 한국 언론 지형 파악_정치인과 주요 이슈를 중심으로

## 🖥 역할 
- 아이디어, 프로젝트 과정 설계, 데이터 수집(Scrapping), 전처리, 워드 클라우드

<br/> 

### 1. 프로젝트 소개
- **WordCloud**
   - 언론사의 정치적 성향 별로 사회적 이슈에 대해 어떤 어휘를 사용하는지 파악
- **MLP**
   - 많이 접하는 언론사이지만, 정치적 성향이 어떠한지 알 수 없었던 언론사들에 대한 이진분류
    
<br/>

### 2. 언론사 선정 
1. 보수 언론
   - **조선일보, 중앙일보, 동아일보**
2. 진보 언론
   - **한겨례, 경향신문, 오마이뉴스**
3. 기타 언론
   - **매일경제, 머니투데이, 연합뉴스**
  
<br/>

### 3. 키워드
1. 국내 정치인
   - **윤석열, 문재인, 이재명, 한동훈, 추미애, 이준석, 유승민, 심상정**
2. 국외 정치인
   - **김정은, 바이든, 김여정, 트럼프, 기시다, 아베**
3. 사건 사고
   - **해병대, 채상병, 의대증원, 후쿠시마 오염수, 장애인, 노조, 파업, 이재용**

<br/>

### 4. 데이터 수집

**[네이버 뉴스 API]**

- 네이버 뉴스 API에서 언론사를 필터링하는 파라미터 제공 X
- 키워드 앞에 언론사 명을 붙여 수집하기로 결정 (ex.한겨레 후쿠시마 오염수)

<br/>

**[특정 언론사의 기사만 수집]**

- 단순히 검색 키워드 앞에 언론사명을 붙였기 때문에 언론사 필터링이 잘 되어있지 않음
   - ex) '오마이뉴스 후쿠시마' 검색 결과에 오마이뉴스 외 언론사 기사가 존재

- 특정 언론사 네이버 뉴스 base link를 통해 특정 언론사 기사만 필터링
   - ex) '오마이뉴스 후쿠미사' 검색 결과에 오마이뉴스 기사만 가져오기

<br/>

**[selenium을 통해 기사 제목 및 링크 수집]**

- 각 언론사별 네이버 뉴스 링크를 하나씩 접속하여 기사 제목 및 링크 수집 **(약 63,000개)**

<br/>

### 5. 전처리

**[공통]**
   - 한글과 공백을 제외한 모든 문자 제거
   - 연속된 공백을 단일 공백으로 변환
   - 양쪽 끝의 공백 문자 제거
   - stopwords 제거

**[MLP]**
   - 진보, 보수 성향 데이터프레임에 label 값 할당 (진보:1 , 보수:0)
   - 분류 모델 학습에 있어 특정 언론사명이 개입되지 않도록 기사 제목에서 언론사명 모두 삭제
   - 진보, 보수 데이터 불균형이 존재하여 **한국어 BERT 모델을 통한 Data Augmentation 수행**                                                                                               
     - **random masking replacement, random masking insertion**

<br/>

### 6. WordCloud 생성

- 전처리된 언론사별 제목을 하나의 text로 이어붙여 진보,기타,보수 언론 순으로 WordCloud 생성

![6-1](https://github.com/user-attachments/assets/a383c5bb-f6af-46ec-8077-7261f067bbe0)
![6-2](https://github.com/user-attachments/assets/37e8ff3f-d88a-4a48-8aae-b475e785fbb4)

<br/>

### 7. MLP

**[모델 구성]**
   - 4개의 hideen layer와 1개의 output layer
   - Fully Connected Layer
   - Batch Normalization
   - 활성화 함수 ReLU 적용 후 Dropout 적용(p=0.5)

<br/>

**[모델 학습]**
   - 데이터의 20%를 test data로 사용
   - batch size=32
   - 은닉층의 뉴런수를 절반씩 줄여나감
   - 이진 분류(진보,보수)를 위해 출력층의 뉴런 수를 2로 설정
   - 손실함수는 CrossEntropyLoss, Optimizer는 Adam

<br/>

**[Word2Vec]**
   - 모델 정확도 평균 58.05%로 성능이 좋지 않음
   - epoch과 hidden layer 수를 늘려봤지만 크게 효과가 없었음

<br/>

**[TF-IDF]**
   - 모델 정확도 평균 82.55% (최대 94.29%)로 약 24.5% 정확도 상승
   - TF-IDF 벡터로 학습시킨 모델을 통해 연합뉴스, 매일경제, 머니투데이의 성향을 파악하기로 결정

<br/>

**[우리만의 해석]**
   - 기사 제목은 일반적으로 짧고 핵심 단어로 이루어져 있음
   - TF-IDF는 특정 문서에서만 자주 등장하는 단어의 가중치는 높임
   - 이는 짧은 텍스트에서 단어의 중요도를 명확하게 반영할 수 있음
   - 반면 Word2Vec은 단어의 문맥을 반영하여 단어 벡터를 학습
   - 따라서 짧은 텍스트에서는 충분한 문맥 정보를 얻기 어려움

<br/>

**[예측 결과]**
   - 윤석열 (세 언론사 모두 진보 성향)

![6-3](https://github.com/user-attachments/assets/04c61d37-4fef-4e0c-8467-771d084e3640)

   - 이재명 (세 언론사 모두 진보 성향)
     
![6-4](https://github.com/user-attachments/assets/118ced89-b914-4ab3-8238-b8ecb2152773)

<br/>

**[계속해서 논의할 사항]**
- MLP 모델이 test media(연합뉴스,매일경제,머니투데이)가 특정키워드에서 대부분 '진보성향'을 나타내고 있다고 하지만 이를 그대로 받아드리면 안됨
- count가 적은 결과는 표본 수가 적기 때문에 큰 의미부여를 하면 안됨
- BERT Augmentation은 주로 보수 진영 기사에서 이루어졌고 잘못된 증강이 되었을 가능성 존재하여 편향된 결과가 나왔을 가능성 있음
- **따라서 데이터 불균형에 대한 해결방안은 계속해서 생각해보고 개선해야 될 사항임**

