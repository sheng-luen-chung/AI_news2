# update_news.py
import re
import arxiv
import json
import os
from gtts import gTTS
from datetime import datetime
import google.generativeai as genai

NEWS_PATH = "news.jsonl"
PROCESSED_IDS_PATH = "processed_ids.txt"

# === 設定 Gemini API 金鑰 ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# === 輔助函式：讀取與儲存已處理的 ID ===
def load_processed_ids(path=PROCESSED_IDS_PATH):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_processed_ids(ids, path=PROCESSED_IDS_PATH):
    with open(path, "w") as f:
        f.write("\n".join(ids))

# === 抓取 AI 論文摘要 ===
def fetch_ai_papers(query="ai", max_results=25):
    processed_ids = load_processed_ids()
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in client.results(search):
        # 跳過已處理的論文
        if result.get_short_id() in processed_ids:
            continue
        papers.append({
            "id": result.get_short_id(),
            "url": result.entry_id,
            "title": result.title,
            "summary": result.summary,
            "authors": [author.name for author in result.authors],
            "published_date": result.published.strftime("%Y-%m-%d")
        })
        # 將新處理的 ID 添加到集合中
        processed_ids.add(result.get_short_id())
        # 只抓取1篇
        break

    # 在處理完所有論文後，一次性儲存更新後的 ID 集合
    save_processed_ids(processed_ids)
    return papers

# === 使用 Gemini 摘要為繁體中文 ===
def summarize_to_chinese(title, summary):
    prompt = (
        f"請將以下arXiv論文標題與摘要翻譯成繁體中文，"
        f"並將摘要濃縮成適合收聽且簡明扼要的中文摘要。\n"
        f"英文標題：{title}\n"
        f"英文摘要：{summary}\n"
        f"請用JSON格式回覆，例如：{{\"title_zh\": \"...\", \"summary_zh\": \"...\"}}"
    )
    response = model.generate_content(prompt)
    text = response.text.strip()
    # 移除可能的 markdown 程式碼區塊標記
    text = re.sub(r"^```json|^```|```$", "", text, flags=re.MULTILINE).strip()
    # 解析 JSON 回應
    result = json.loads(text)
    return result

# === 將摘要轉成語音檔 ===
def save_audio(text, filename):
    tts = gTTS(text, lang='zh-tw')
    tts.save(filename)

# === 主流程 ===
def main():
    os.makedirs("audios", exist_ok=True)
    
    print("正在抓取 arxiv 文章...")
    papers = fetch_ai_papers(query="ai", max_results=25)
    print(f"抓取到 {len(papers)} 篇文章")
    
    if(len(papers) > 0):
        for i, paper in enumerate(papers):
            print(f"正在翻譯第 {i+1} 篇：{paper['title']}")
            result = summarize_to_chinese(paper['title'], paper['summary'])
            
            audio_path = f"audios/{paper['id']}.mp3"
            save_audio(result['title_zh'] + "\n" + result['summary_zh'], audio_path)

            # 保留原始資料並新增中文和音訊資訊
            paper_data = paper.copy()  # 複製原始資料
            paper_data.update({
                "title_zh": result['title_zh'],
                "summary_zh": result['summary_zh'],
                "audio": audio_path,
                "timestamp": datetime.now().isoformat()
            })
            
            # 直接將新文章附加到檔案末尾
            with open(NEWS_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(paper_data, ensure_ascii=False) + "\n")

        print("✅ 更新完成：news.json 和 MP3 音檔已產生")

if __name__ == "__main__":
    main()
