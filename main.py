import requests
import whisper
import os
import re

def run():
    # 股癌 Firstory RSS
    rss_url = "https://open.firstory.me/rss/user/ck9v6941v8d7y0873as9967l8"
    
    print("正在獲取最新集數資訊...")
    resp = requests.get(rss_url, timeout=30)
    content = resp.text

    # 暴力法抓取標題與連結，避開所有 XML 解析問題
    try:
        title = re.search(r'<item>.*?<title>(.*?)</title>', content, re.S).group(1)
        audio_url = re.search(r'<enclosure.*?url="(.*?)"', content, re.S).group(1)
    except Exception:
        print("解析失敗，嘗試備用方案...")
        title = "Gooaye_Latest"
        audio_url = re.search(r'url="(https://[^"]+?\.mp3[^"]*?)"', content).group(1)

    # 檔名純化
    clean_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)
    os.makedirs("transcripts", exist_ok=True)
    
    print(f"正在下載音檔: {title}")
    audio_data = requests.get(audio_url).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("AI 轉錄中 (Whisper Base)...")
    model = whisper.load_model("base")
    result = model.transcribe("temp.mp3", initial_prompt="這是股癌 Gooaye 的投資分析，討論台股、美股與產業研究。", fp16=False)
    
    file_path = f"transcripts/{clean_title}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(result["text"])
    
    print(f"成功！已產出: {file_path}")
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

if __name__ == "__main__":
    run()
