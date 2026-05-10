import requests
import re
import whisper
import os
import datetime

def run():
    # 使用 Apple Podcast 的 RSS 源，這絕對不會要求登入或擋機器人
    rss_url = "https://feeds.megaphone.fm/WWO8022634352"
    
    print("正在獲取集數資訊...")
    headers = {'User-Agent': 'Podcast/1.0'}
    resp = requests.get(rss_url, headers=headers, timeout=30)
    content = resp.text

    # 提取最新的音檔網址
    try:
        audio_url = re.search(r'url="(https://[^"]+?\.mp3[^"]*?)"', content).group(1)
        today = datetime.datetime.now().strftime("%Y%m%d")
        title = f"Gooaye_{today}"
    except Exception as e:
        print(f"提取失敗: {e}")
        return

    # 確保資料夾存在
    os.makedirs("transcripts", exist_ok=True)
    
    print(f"正在下載音檔...")
    audio_data = requests.get(audio_url, headers=headers).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("AI 轉錄中 (使用 Whisper Base)... 這步最關鍵...")
    model = whisper.load_model("base")
    result = model.transcribe("temp.mp3", initial_prompt="這是股癌 Gooaye 的投資分析。", fp16=False)
    
    # 強制寫入檔案
    file_path = os.path.join("transcripts", f"{title}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{result['text']}")
    
    print(f"檔案已成功產出至: {file_path}")
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

if __name__ == "__main__":
    run()
