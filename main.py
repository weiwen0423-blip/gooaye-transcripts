import requests
import re
import whisper
import os
import datetime

def run():
    rss_url = "https://feeds.megaphone.fm/WWO8022634352"
    headers = {'User-Agent': 'Podcast/1.0'}
    
    print("正在獲取集數...")
    resp = requests.get(rss_url, headers=headers, timeout=30)
    
    # 提取音檔連結
    audio_url = re.search(r'url="(https://[^"]+?\.mp3[^"]*?)"', resp.text).group(1)
    
    # 使用日期作為檔名，確保不會重複
    today = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"Gooaye_{today}.md"
    
    # 【關鍵】使用絕對路徑，確保檔案寫在 transcripts 資料夾
    current_dir = os.getcwd()
    target_dir = os.path.join(current_dir, "transcripts")
    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, filename)

    print(f"正在下載音檔...")
    audio_data = requests.get(audio_url, headers=headers).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("AI 轉錄中... 這步最久，請耐心等候...")
    model = whisper.load_model("base")
    result = model.transcribe("temp.mp3", initial_prompt="這是股癌 Gooaye 的投資分析。", fp16=False)
    
    # 寫入檔案
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {filename}\n\n{result['text']}")
    
    # 檢查檔案是否真的產出了
    if os.path.exists(file_path):
        print(f"✅ 成功產出檔案：{file_path}，大小：{os.path.getsize(file_path)} bytes")
    else:
        print("❌ 檔案產出失敗！")
        exit(1) # 讓 Action 變紅燈報錯

    os.remove("temp.mp3")

if __name__ == "__main__":
    run()
