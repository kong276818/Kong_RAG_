import json
import re
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# KoBART 요약 모델 로딩
tokenizer = AutoTokenizer.from_pretrained("digit82/kobart-summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("digit82/kobart-summarization")

def summarize_korean(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    input_ids = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        input_ids,
        max_length=128,
        min_length=32,
        num_beams=4,
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def process_and_summarize(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        try:
            text = item.get("text", "")
            item["summary"] = summarize_korean(text)
        except Exception as e:
            item["summary"] = f"요약 실패: {str(e)}"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f" 요약 저장 완료: {output_path}")

#  실행 예시
if __name__ == "__main__":
    process_and_summarize("data.json", "data_with_summary.json")
