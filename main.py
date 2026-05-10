import feedparser
import requests
import whisper
import os
import re

def slugify(text):
    # 更嚴格的字元過濾，只保留中文、英文與數字
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
    return text.strip().replace(' ', '_')

def run():
    rss_url = "https://feeds.megaphone.fm/WWO8022634352" 
    print("正在獲取 Podcast 更新清單...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        resp = requests.get(rss_url, headers=headers, timeout=30)
        feed = feedparser.parse(resp.content)
        
        if not feed.entries:
            print("錯誤：抓不到集數")
            return

        latest_episode = feed.entries[0]
        audio_url = latest_episode.enclosures[0].href
        original_title = latest_episode.title
        clean_title = slugify(original_title)
        
        print(f"發現最新一集: {original_title}")
        
        # 建立資料夾
        if not os.path.exists("transcripts"):
            os.makedirs("transcripts")
            print("已建立 transcripts 資料夾")

        # 下載音檔
        print("正在下載音檔...")
        audio_data = requests.get(audio_url).content
        with open("temp.mp3", "wb") as f:
            f.write(audio_data)
        
        print("正在啟動 AI 辨識...")
        model = whisper.load_model("base")
        result = model.transcribe("temp.mp3", initial_prompt="這是股癌 Gooaye 的投資分析。", fp16=False)
        
        # 強制寫入檔案
        file_path = os.path.join("transcripts", f"{clean_title}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {original_title}\n\n")
            f.write(result["text"])
        
        # 檢查檔案是否真的存在
        if os.path.exists(file_path):
            print(f"確認成功！檔案已產生於: {file_path}")
        else:
            print("警告：檔案寫入失敗！")
            
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        if os.path.exists("temp.mp3"):
            os.remove("temp.mp3")

if __name__ == "__main__":
    run()
