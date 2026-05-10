import feedparser
import requests
import whisper
import os
import re

def run():
    # 使用穩定來源
    rss_url = "https://feeds.megaphone.fm/WWO8022634352"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(rss_url, headers=headers)
    feed = feedparser.parse(resp.content)
    
    if not feed.entries:
        raise Exception("找不到 Podcast 集數")

    latest = feed.entries[0]
    # 簡化標題避免非法字元
    clean_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', latest.title)
    
    # 建立資料夾
    os.makedirs("transcripts", exist_ok=True)
    
    print(f"下載中: {latest.title}")
    audio_data = requests.get(latest.enclosures[0].href).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("辨識中...")
    model = whisper.load_model("base")
    result = model.transcribe("temp.mp3", initial_prompt="股癌投資分析", fp16=False)
    
    # 產出檔案
    with open(f"transcripts/{clean_title}.md", "w", encoding="utf-8") as f:
        f.write(f"# {latest.title}\n\n{result['text']}")
    
    # 確認檔案真的在那裡
    print(f"目前資料夾內容: {os.listdir('transcripts')}")
    os.remove("temp.mp3")

if __name__ == "__main__":
    run()
