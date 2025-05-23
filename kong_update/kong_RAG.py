import os
import json
import time
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# 문서 로드
def load_docs(json_path):
    if not os.path.exists(json_path):
        return []
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 새로운 쿼리가 기존 문서에 없다면 문서를 자동 추가
def add_new_doc_if_needed(query, docs, json_path, doc_type):
    query_lower = query.lower()
    for doc in docs:
        combined = " ".join([
            doc.get("case_id", ""),
            doc.get("text", ""),
            doc.get("timestamp", ""),
            doc.get("q", "")
        ]).lower()
        if query_lower in combined:
            return docs  # 이미 있음

    # 새로운 문서 자동 생성
    new_doc = {
        "case_id": f"C{str(len(docs) + 1).zfill(4)}",
        "type": doc_type,
        "text": query,
        "timestamp": datetime.now().strftime("%Y-%m-%d"),
        "summary": query,  # 최초 입력 쿼리를 임시 요약으로 설정
        "q": query  # 키워드도 동일하게 초기화
    }
    docs.append(new_doc)

    # 저장
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)

    print(f" 새 문서 추가됨: {new_doc['case_id']}")
    return docs

#  정확 매칭 요약 반환
def exact_match_summary(query, docs):
    query = query.lower()
    for doc in docs:
        combined = " ".join([
            doc.get("case_id", ""),
            doc.get("text", ""),
            doc.get("timestamp", ""),
            doc.get("q", "")
        ]).lower()
        if query in combined:
            return doc.get("summary", "")
    return None

#  모델 예측 summary 및 유사도 측정
def model_predict_summary_and_text_similarity(query, docs, model):
    query_embedding = model.encode(query, convert_to_tensor=True)

    summaries = [doc.get("summary", "") for doc in docs]
    texts = [doc.get("text", "") for doc in docs]

    summary_embeddings = model.encode(summaries, convert_to_tensor=True)
    text_embeddings = model.encode(texts, convert_to_tensor=True)

    summary_scores = util.cos_sim(query_embedding, summary_embeddings)[0]
    best_idx = summary_scores.argmax().item()

    best_summary = summaries[best_idx]
    best_text = texts[best_idx]
    summary_score = summary_scores[best_idx].item()

    # 쿼리 ↔ 문서 전체 텍스트 유사도 측정
    text_score = util.cos_sim(query_embedding, text_embeddings[best_idx])[0].item()

    return best_summary, summary_score, text_score

#  메인 실행
if __name__ == "__main__":
    doc_type = input("문서 유형 선택 (chat / meeting / law): ").strip().lower()
    if doc_type not in ["chat", "meeting", "law"]:
        print(" chat / meeting / law 중 하나만 입력하세요.")
        exit(1)

    json_path = f"output_docs/{doc_type}_docs.json"
    print(" 문서 로딩 중...")
    docs = load_docs(json_path)

    print(" 모델 로딩 중...")
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    while True:
        query = input("\n 쿼리를 입력하세요 (종료하려면 'exit'): ").strip()
        if query.lower() == "exit":
            print(" 종료합니다.")
            break

        # 새 쿼리에 대해 문서 자동 추가 (필요한 경우만)
        docs = add_new_doc_if_needed(query, docs, json_path, doc_type)

        start_time = time.time()

        # 정확 매칭 우선
        exact = exact_match_summary(query, docs)
        if exact:
            elapsed = time.time() - start_time
            print("\n [정확 매칭 Summary]")
            print(exact)
            print(f"\n 소요 시간: {elapsed:.3f}초")
            continue

        # 정확 매칭 실패 → 모델 예측
        predicted_summary, summary_score, text_score = model_predict_summary_and_text_similarity(query, docs, model)
        elapsed = time.time() - start_time

        print("\n [모델 예측 Summary]")
        print(predicted_summary)

        print(f"\n 유사도 분석:")
        print(f"- 쿼리 ↔ 예측 Summary 유사도: {summary_score:.4f}")
        print(f"- 쿼리 ↔ 예측 문서 전체 Text 유사도: {text_score:.4f}")
        print(f" 소요 시간: {elapsed:.3f}초")