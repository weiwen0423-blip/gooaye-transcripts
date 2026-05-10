import yt_dlp
import whisper
import os
import datetime
import re

def run():
    url = "https://www.youtube.com/@Gooaye/videos"
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'noplaylist': True,
        'playlist_items': '1',
        'nocheckcertificate': True,
        'quiet': True,
        'outtmpl': 'latest_audio.m4a',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("正在連線至 YouTube...")
            info = ydl.extract_info(url, download=True)
            title = info['entries'][0]['title']
        
        # 清理標題字元避免存檔失敗
        clean_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)
        os.makedirs("transcripts", exist_ok=True)
        
        print(f"辨識中: {title}")
        model = whisper.load_model("base")
        # 針對基本面研究加入導引詞
        result = model.transcribe("latest_audio.m4a", initial_prompt="股癌,台股,美股,CoWoS,標的,展望", fp16=False)
        
        now = datetime.datetime.now().strftime("%Y%m%d")
        file_path = f"transcripts/Gooaye_{now}_{clean_title}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{result['text']}")
        
        print(f"成功產出: {file_path}")
        
    except Exception as e:
        print(f"錯誤: {e}")
        raise e
    finally:
        if os.path.exists("latest_audio.m4a"):
            os.remove("latest_audio.m4a")

if __name__ == "__main__":
    run()
