import feedparser
import requests
import whisper
import os
import re

def slugify(text):
    return re.sub(r'[\\/:*?"<>|]', '_', text)

def run():
    # 改用 Apple Podcast 體系的 RSS，通常更穩定
    rss_url = "https://feeds.megaphone.fm/WWO8022634352" 
    
    print("正在獲取 Podcast 更新清單...")
    # 偽裝成瀏覽器，避免被擋
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        resp = requests.get(rss_url, headers=headers, timeout=30)
        feed = feedparser.parse(resp.content)
        
        if not feed.entries:
            print("錯誤：抓不到任何集數，請檢查 RSS 連結")
            return

        # 抓取最新一集
        latest_episode = feed.entries[0]
        audio_url = latest_episode.enclosures[0].href
        original_title = latest_episode.title
        title = slugify(original_title)
        
        print(f"發現最新一集: {original_title}")
        
        # 下載音檔
        print("正在下載音檔...")
        audio_resp = requests.get(audio_url, stream=True)
        with open("latest_audio.mp3", "wb") as f:
            for chunk in audio_resp.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("正在啟動 AI 辨識（Whisper base）...")
        model = whisper.load_model("base")
        # 加入 initial_prompt 強化財經術語辨識
        result = model.transcribe("latest_audio.mp3", initial_prompt="這是股癌 Gooaye 的投資分析，包含台股、美股、半導體、供應鏈、CoWoS、AI 伺服器等討論。", fp16=False)
        
        if not os.path.exists("transcripts"):
            os.makedirs("transcripts")
            
        file_path = f"transcripts/{title}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {original_title}\n\n")
            f.write(f"> 原始連結: {audio_url}\n\n")
            f.write(result["text"])
        
        print(f"成功！逐字稿已存至: {file_path}")
        
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        if os.path.exists("latest_audio.mp3"):
            os.remove("latest_audio.mp3")

if __name__ == "__main__":
    run()
