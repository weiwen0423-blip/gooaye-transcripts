import requests
import whisper
import os
import datetime

def run():
    # 改用股癌最穩定的 RSS 並直接針對音檔標籤進行最保險的切割
    rss_url = "https://open.firstory.me/rss/user/ck9v6941v8d7y0873as9967l8"
    
    print("正在獲取資料...")
    resp = requests.get(rss_url, timeout=30)
    content = resp.text

    # 1. 直接尋找第一個 mp3 連結 (這是最新一集)
    try:
        audio_url = content.split('url="')[1].split('"')[0]
        # 2. 隨機生成一個標題避免解析失敗
        today = datetime.date.today().strftime("%Y%m%d")
        title = f"Gooaye_Episode_{today}"
    except Exception as e:
        print(f"提取失敗: {e}")
        return

    os.makedirs("transcripts", exist_ok=True)
    
    print(f"下載音檔: {audio_url}")
    audio_data = requests.get(audio_url).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("AI 轉錄中 (Whisper Base)...")
    model = whisper.load_model("base")
    # 強制繁體中文導向
    result = model.transcribe("temp.mp3", initial_prompt="這是股癌 Gooaye Podcast 的逐字稿。", fp16=False)
    
    file_path = f"transcripts/{title}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"> 來源連結: {audio_url}\n\n")
        f.write(result["text"])
    
    print(f"成功！已產出: {file_path}")
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

if __name__ == "__main__":
    run()
