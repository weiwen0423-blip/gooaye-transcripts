import requests
import feedparser
import whisper
import os
import re

def run():
    # 這是 Megaphone 的直接 RSS，最穩定且不擋機器人
    url = "https://feeds.megaphone.fm/WWO8022634352"
    
    # 偽裝成一般的播放器 (如同 Apple Podcast App)
    headers = {'User-Agent': 'Podcast/1.0'}
    
    print("正在獲取最新集數資訊...")
    resp = requests.get(url, headers=headers)
    feed = feedparser.parse(resp.content)
    
    if not feed.entries:
        raise Exception("無法讀取集數資訊，請檢查連結")

    item = feed.entries[0]
    title = item.title
    audio_url = item.enclosures[0].href
    
    # 檔名純化，只留中英文字
    clean_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)
    os.makedirs("transcripts", exist_ok=True)
    
    print(f"下載中: {title}")
    audio_data = requests.get(audio_url, headers=headers).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("AI 轉錄中 (使用 Whisper Base)...")
    model = whisper.load_model("base")
    # 加入你最在意的投資標的關鍵字，讓 AI 辨識更準
    result = model.transcribe("temp.mp3", initial_prompt="股癌,台股,美股,半導體,CoWoS,供應鏈,投資標的,主委", fp16=False)
    
    file_path = f"transcripts/{clean_title}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(result["text"])
    
    print(f"成功！檔案已產出: {file_path}")
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

if __name__ == "__main__":
    run()
