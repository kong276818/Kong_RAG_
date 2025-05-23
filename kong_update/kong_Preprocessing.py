import json
from pathlib import Path

def normalize_and_split_types(input_path: str, output_dir: str):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 분류용 딕셔너리
    split_data = {
        "chat": [],
        "meeting": [],
        "law": []
    }

    for item in data:
        # type 정규화: meet → meeting
        raw_type = item.get("type", "").lower()
        doc_type = "meeting" if raw_type == "meet" else raw_type

        # q 필드 평탄화
        keywords = item.get("q", [])
        item["q"] = ", ".join(keywords)

        if doc_type in split_data:
            item["type"] = doc_type  # 타입 필드도 일관성 있게 수정
            split_data[doc_type].append(item)

    # 저장 디렉토리 생성
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 각 타입별 파일 저장
    for doc_type, docs in split_data.items():
        out_path = Path(output_dir) / f"{doc_type}_docs.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2, ensure_ascii=False)
        print(f"✅ 저장 완료: {out_path} ({len(docs)}건)")

# 실행 예시
if __name__ == "__main__":
    normalize_and_split_types("data_with_summary_keywords.json", "output_docs")
