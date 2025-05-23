import json
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text: str, top_k: int = 5) -> list:
    vectorizer = TfidfVectorizer(max_features=1000, token_pattern=r"(?u)\b\w+\b", stop_words=["있다", "한다", "수", "등", "및", "위해"])
    X = vectorizer.fit_transform([text])
    scores = X.toarray().flatten()
    keywords = [
        word for word, score in sorted(zip(vectorizer.get_feature_names_out(), scores), key=lambda x: x[1], reverse=True)
        if score > 0
    ][:top_k]
    return keywords

def enrich_with_keywords(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        base_text = item.get("summary", item.get("text", ""))
        keywords = extract_keywords(base_text)
        item["q"] = keywords

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f" 키워드 필드(q) 추가 완료 → {output_path}")

# 실행 예시
if __name__ == "__main__":
    enrich_with_keywords("data_with_summary.json", "data_with_summary_keywords.json")
