import requests
import whisper
import os
import datetime

def run():
    rss_url = "https://open.firstory.me/rss/user/ck9v6941v8d7y0873as9967l8"
    print("正在獲取最新集數...")
    resp = requests.get(rss_url, timeout=30)
    content = resp.text

    try:
        audio_url = content.split('url="')[1].split('"')[0]
        today = datetime.date.today().strftime("%Y%m%d")
        title = f"Gooaye_{today}"
    except Exception as e:
        print(f"失敗: {e}")
        return

    # 使用絕對路徑確保沒人搞丟
    current_dir = os.getcwd()
    save_dir = os.path.join(current_dir, "transcripts")
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"下載中...")
    audio_data = requests.get(audio_url).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("辨識中 (Whisper)...")
    model = whisper.load_model("base")
    result = model.transcribe("temp.mp3", initial_prompt="股癌投資分析", fp16=False)
    
    file_path = os.path.join(save_dir, f"{title}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{result['text']}")
    
    print(f"確認產出檔案於: {file_path}")
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

if __name__ == "__main__":
    run()
