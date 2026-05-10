import requests
import xml.etree.ElementTree as ET
import whisper
import os
import re

def run():
    # 這是股癌在 Firstory 的原始 RSS 連結
    rss_url = "https://open.firstory.me/rss/user/ck9v6941v8d7y0873as9967l8"
    
    print("正在獲取最新集數資訊...")
    resp = requests.get(rss_url, timeout=30)
    # 直接解析 XML，不靠第三方套件，最穩
    root = ET.fromstring(resp.content)
    item = root.find('.//item')
    
    title = item.find('title').text
    audio_url = item.find('enclosure').attrib['url']
    
    # 檔名純化
    clean_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)
    os.makedirs("transcripts", exist_ok=True)
    
    print(f"正在下載音檔: {title}")
    audio_data = requests.get(audio_url).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("AI 轉錄中 (使用 Whisper Base)...")
    model = whisper.load_model("base")
    # 強制使用繁體中文 prompt
    result = model.transcribe("temp.mp3", initial_prompt="這是股癌 Gooaye 的 Podcast，討論台股、美股與產業研究。", fp16=False)
    
    file_path = f"transcripts/{clean_title}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(result["text"])
    
    print(f"成功！已產出: {file_path}")
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

if __name__ == "__main__":
    run()
