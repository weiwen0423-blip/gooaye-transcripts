import yt_dlp
import whisper
import os

# 這裡先設定一個範例，之後可以改成自動抓最新影片
def run():
    url = "https://www.youtube.com/@Gooaye/videos" # 股癌頻道
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'playlist_items': '1', # 只抓最新的一支影片
        'outtmpl': 'latest_audio.m4a',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info['entries'][0]['title']
    
    print(f"正在轉錄: {title}")
    model = whisper.load_model("base")
    result = model.transcribe("latest_audio.m4a", initial_prompt="以下是繁體中文內容")
    
    # 儲存成 Markdown 格式，方便之後架站
    with open(f"transcripts/{title}.md", "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(result["text"])

if __name__ == "__main__":
    if not os.path.exists("transcripts"):
        os.makedirs("transcripts")
    run()
