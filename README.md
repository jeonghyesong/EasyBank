# EasyBank AI 프로젝트

고령층을 위한 자연어 기반 금융 서비스 챗봇입니다.
이 프로젝트는 인텐트 분류, 슬롯 추출, 쉬운말 변환 모델을 활용해 사용자의 발화를 이해하고 송금, 예금, 대출, 카드 서비스 등의 기능을 제공합니다.

---

## 📁 폴더 구조

* `model/` : AI 모델 정의 및 학습 결과(구조 파일 `config.json`, 토크나이저 설정 등)
* `backend/` : FastAPI 기반 백엔드 서버 코드
* `frontend/` : 사용자 인터페이스(UI) 코드
* `scripts/` : 데이터 파이프라인 및 학습·배포 자동화 스크립트

  * `run.py` : train → evaluate → push\_to\_hub 전체 워크플로우 실행
  * `data_crawl.py` : Raw 데이터 수집
  * `data_preprocessing.py` : 전처리 과정 실행
* `data/` : 학습 및 서비스용 데이터 파일

---

## 🔄 데이터 파이프라인 요약

1. **Raw 데이터 수집**
   * 스크립트: `scripts/data_crawl.py` 실행
   * 출력 파일: `data/kb_financial_terms.csv`
   * 수기 검수 후 저장: `data/manual_data.csv`

2. **최종 전처리**
   * 스크립트: `scripts/data_preprocessing.py` 실행
   * 입력 파일: `data/manual_data.csv`
   * 출력 파일: `data/clean_data.csv`

3. **모델 학습·평가·배포**
   * 스크립트: `scripts/run.py` 실행
     python scripts/run.py
   * 내부 단계:
     1. `train()` → 학습
     2. `evaluate()` → 검증
     3. `push_to_hub()` → Hugging Face Hub 업로드




