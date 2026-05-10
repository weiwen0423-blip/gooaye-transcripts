import feedparser
import requests
import whisper
import os

def run():
    # 這是股癌的 Podcast RSS 連結
    rss_url = "https://feeds.soundon.fm/podcasts/7e7732a3-85f0-437a-9a9c-09758784cf2b.xml"
    feed = feedparser.parse(rss_url)
    
    # 抓取最新一集
    latest_episode = feed.entries[0]
    audio_url = latest_episode.enclosures[0].href
    title = latest_episode.title
    
    print(f"正在從 Podcast 下載: {title}")
    
    # 下載音檔
    response = requests.get(audio_url)
    with open("latest_audio.mp3", "wb") as f:
        f.write(response.content)
    
    print(f"正在轉錄...")
    model = whisper.load_model("base")
    result = model.transcribe("latest_audio.mp3", initial_prompt="以下是繁體中文內容")
    
    if not os.path.exists("transcripts"):
        os.makedirs("transcripts")
        
    with open(f"transcripts/{title}.md", "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(result["text"])
    
    os.remove("latest_audio.mp3")

if __name__ == "__main__":
    run()
