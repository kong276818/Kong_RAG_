# Kong_RAG_

**상상력을 구조화하고 전략으로 구현하는 것**  
문서를 읽고, 의미를 이해하며, 전략까지 제시하는 RAG 기반 규제 대응 자동화 시스템

---

## 📌 개요 (Overview)

**Kong_RAG_**는 규제 기관 대응, 정책 문서 정리, 내부 질의 자동화 등을 위한  
의미 기반 검색 + 생성형 응답 시스템입니다.  
문서 요약, 키워드 추출, 임베딩 검색, LLM 응답 생성까지 하나의 파이프라인으로 통합되어  
실제 업무 현장에서도 바로 적용 가능한 구조를 갖추고 있습니다.

---

## 🔍 주요 기능 (Features)

- 📄 **KoBART** 기반 문서 요약
- 🧠 **TF-IDF** 키워드 추출
- 🔗 **SentenceTransformer** 임베딩 생성
- 📚 의미 유사도 기반 **Top-K 문서 검색**
- 🤖 **KoAlpaca** 또는 **GPT** 응답 생성
- 🗂 문서 유형 구분(chat / law / meeting 등)
- 💾 **FAISS** 기반 벡터 DB 인덱싱

---

## 📁 디렉토리 구조 (Structure)


Kong_RAG_/
├── data/ # 원천 문서 (JSON 등)
├── summary/ # 생성된 요약 및 키워드
├── index/ # FAISS 인덱스 저장소
├── model/ # 임베딩 및 LLM 구성
├── app.py # 메인 실행 코드
└── README.md # 프로젝트 소개 문서


---

## 🚀 사용 예시 (Usage)

```bash
python app.py --query "2024년 공정위 경고 관련 사내 대응 사례는?"

```

📌 저자
공준영 (Kong276818)
문의: kong745869@naver.com
