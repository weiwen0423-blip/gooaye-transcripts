import yt_dlp
import whisper
import os
import datetime

def run():
    # 股癌頻道的影音列表連結
    url = "https://www.youtube.com/@Gooaye/videos"
    
    # 強力偽裝參數，讓 YouTube 覺得你是真人
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'noplaylist': True,
        'playlist_items': '1', # 永遠只抓最新的一集
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'outtmpl': 'latest_audio.m4a',
        # 使用瀏覽器身分標記
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("正在透過 YouTube 提取最新集數...")
            info = ydl.extract_info(url, download=True)
            title = info['entries'][0]['title']
        
        print(f"成功下載: {title}")
        now = datetime.datetime.now().strftime("%Y%m%d")
        os.makedirs("transcripts", exist_ok=True)
        
        print("AI 轉錄中... 這步最慢，請稍候...")
        model = whisper.load_model("base")
        # 針對主委常講的術語做 prompt 優化
        result = model.transcribe("latest_audio.m4a", initial_prompt="股癌,台股,美股,CoWoS,半導體,標的,展望", fp16=False)
        
        file_path = f"transcripts/Gooaye_{now}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{result['text']}")
        
        print(f"--- 完成！檔案已存於: {file_path} ---")
        
    except Exception as e:
        print(f"致命錯誤: {e}")
        raise e
    finally:
        if os.path.exists("latest_audio.m4a"):
            os.remove("latest_audio.m4a")

if __name__ == "__main__":
    run()
