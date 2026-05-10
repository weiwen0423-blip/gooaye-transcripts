import yt_dlp
import whisper
import os
import re

def run():
    # 股癌 YouTube 頻道影片列表
    url = "https://www.youtube.com/@Gooaye/videos"
    
    # 專門為了繞過機器人檢查的設定
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'noplaylist': True,
        'playlist_items': '1', # 只抓最新一集
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("正在獲取 YouTube 最新影片資訊...")
            info = ydl.extract_info(url, download=True)
            entry = info['entries'][0]
            title = entry['title']
            audio_file = ydl.prepare_filename(entry)

        # 整理標題
        clean_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)
        os.makedirs("transcripts", exist_ok=True)
        
        print(f"辨識中: {title}")
        model = whisper.load_model("base")
        # 這裡加入你最關心的基本面關鍵字，強化 AI 辨識準度
        result = model.transcribe(audio_file, initial_prompt="股癌,台股,美股,半導體,CoWoS,供應鏈,投資標的", fp16=False)
        
        file_path = f"transcripts/{clean_title}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(result["text"])
        
        print(f"成功！已產生: {file_path}")
        if os.path.exists(audio_file):
            os.remove(audio_file)

    except Exception as e:
        print(f"失敗原因: {e}")
        raise e

if __name__ == "__main__":
    run()
