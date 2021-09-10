# ai_traveling_recommend_web
ai허브_codepresso_project(2021.07~2021.08)
## 프로젝트 설명
ai기반 사용자 맞춤 제주도 여행지 추천 웹사이트
## 데이터
- visit_jeju, trip_advisor의 제주도 여행지 댓글 직접 크롤링하여 데이터 수집
- 데이터 수집 후 여행지와 관련없는 데이터 직접 filtering작업 진행

## 모델 구성
1. 여행지 리뷰 텍스트 테마 분석
 - input text : visit_jeju, trip_advisor 사용자 댓글
 - 적용 모델 : bert -> 단순 RNN모델 
    * 수집한 데이터의 양이 데이터 필터링 후 적어졌기 때문에 bert 모델로는 성능이 안나옴 -> RNN을 이용하여 모델 설계
 - output : 각 여행지의 대한 테마별 softmax값 (교육, 레저/체험, 자연)테마로 분류
 
2. 개인감정분석
  - input data : 사용자 기분을 나타낼 수 있는 정면 얼굴 사진
  - 적용 모델
    * 사람 얼굴 인식 : opencv에서 제공하는 사람 얼굴 검출 도구 xml파일 이용
    * 감정 분류 모델 : kaggle face_image data set을 이용하여 cnn기반 모델
  - output:  감정 분류(행복, 슬픔, 화남, 중립) softmax값으로 분류

3. 최종 여행지 추천
  - input_data : 개인 성향 설문, 여행지 분류 SOFTMAX DB, 감정 라벨링 데이터
  - 단순 DNN모델을 이용하여 설계
  - output : 여행지 추천 여부
  
## front-end
- bootstrap과 html, css ,js , jquery이용하여 진행
## back-end
- flask를 이용하여 단순 벡엔드 서버 구성
- aws를 이용하여 infra구축
---



