import requests
import whisper
import os
import datetime

def run():
    # 這是股癌最新的音檔連結 (手動寫死，避開所有解析錯誤)
    audio_url = "https://open.firstory.me/platform/download/ck9v6941v8d7y0873as9967l8/ck9v6941v8d7y0873as9967l8.mp3"
    
    print("正在強制執行轉錄...")
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    title = f"Gooaye_Test_EP_{now}"

    os.makedirs("transcripts", exist_ok=True)
    
    print(f"正在下載音檔...")
    # 加上 headers 避免被擋
    headers = {'User-Agent': 'Mozilla/5.0'}
    audio_data = requests.get(audio_url, headers=headers).content
    
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("正在啟動 AI 辨識 (Whisper Base)...")
    model = whisper.load_model("base")
    result = model.transcribe("temp.mp3", initial_prompt="股癌,台股,美股,投資標的,產業分析", fp16=False)
    
    file_path = os.path.join("transcripts", f"{title}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"生成時間: {now}\n\n")
        f.write(result["text"])
    
    print(f"--- 成功！檔案已產生於: {file_path} ---")
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

if __name__ == "__main__":
    run()
