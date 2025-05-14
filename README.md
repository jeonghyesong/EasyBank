# EasyBank AI 프로젝트
고령층을 위한 자연어 기반 금융 서비스 챗봇입니다.  
이 프로젝트는 인텐트 분류, 정보 추출, 쉬운말 변환 모델을 활용해 사용자의 발화를 이해하고 송금, 예금, 대출, 카드 서비스스 등의 기능을 제공합니다.

## 📁 폴더 구조
- `model/` : AI 모델 학습 코드 및 결과
- `backend/` : FastAPI 기반 API 서버
- `frontend/` : 사용자 UI
- `scripts/` : 크롤링, 전처리 코드
- `data/` : 학습 데이터, 입력 데이터

🔄 데이터 파이프라인 요약
1. Raw 데이터 수집
스크립트: scripts/data_crawl.py 실행
생성 파일: data/kb_financial_terms.csv
2. 수기 편집 단계
원본 파일: data/kb_financial_terms.csv
수기 검수 및 보완하여 저장: data/manual_data.csv
3. 최종 전처리
스크립트: scripts/data_preprocessing.py 실행
입력 파일: data/manual_final.csv
출력 파일: data/final_data.csv


