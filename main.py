import requests
import whisper
import os
import datetime

def run():
    # 直接從 Firstory 抓音檔
    rss_url = "https://open.firstory.me/rss/user/ck9v6941v8d7y0873as9967l8"
    print("正在強制獲取資料...")
    resp = requests.get(rss_url, timeout=30)
    content = resp.text

    # 提取最新的 mp3
    audio_url = content.split('url="')[1].split('"')[0]
    
    # 這裡我們用「精確到秒」的時間命名，確保檔案一定跟上次不同，一定會被 Git 抓到
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    title = f"Gooaye_Full_Transcript_{now}"

    os.makedirs("transcripts", exist_ok=True)
    
    print(f"下載音檔: {audio_url}")
    audio_data = requests.get(audio_url).content
    with open("temp.mp3", "wb") as f:
        f.write(audio_data)
    
    print("啟動 AI 辨識 (Whisper Base)... 這步最耗時...")
    model = whisper.load_model("base")
    result = model.transcribe("temp.mp3", initial_prompt="股癌,台股,美股,基本面,產業研究", fp16=False)
    
    # 寫入 Markdown
    file_path = os.path.join("transcripts", f"{title}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"生成時間: {now}\n\n")
        f.write(result["text"])
    
    # 【關鍵檢查】
    if os.path.exists(file_path) and os.path.getsize(file_path) > 100:
        print(f"--- 成功！檔案大小 {os.path.getsize(file_path)} bytes ---")
    else:
        raise Exception("檔案產生失敗或內容為空！")

    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

if __name__ == "__main__":
    run()
