import feedparser
import requests
import whisper
import os
import re

def slugify(text):
    # 移除非法檔名內容，確保存檔不會報錯
    return re.sub(r'[\\/:*?"<>|]', '_', text)

def run():
    # 股癌 Podcast RSS 連結
    rss_url = "https://feeds.soundon.fm/podcasts/7e7732a3-85f0-437a-9a9c-09758784cf2b.xml"
    print("正在獲取 Podcast 更新清單...")
    feed = feedparser.parse(rss_url)
    
    # 抓取最新一集
    latest_episode = feed.entries[0]
    audio_url = latest_episode.enclosures[0].href
    original_title = latest_episode.title
    title = slugify(original_title)
    
    print(f"正在下載音檔: {original_title}")
    
    # 下載音檔 (使用 mp3 以節省頻寬)
    response = requests.get(audio_url, stream=True)
    with open("latest_audio.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"正在辨識逐字稿（使用 base 模型）...")
    model = whisper.load_model("base")
    # initial_prompt 幫助 AI 減少錯字，並維持繁體中文
    result = model.transcribe("latest_audio.mp3", initial_prompt="這是股癌 Gooaye 的 Podcast，內容包含投資、美股、台股與市場分析。", fp16=False)
    
    # 確保資料夾存在
    if not os.path.exists("transcripts"):
        os.makedirs("transcripts")
        
    # 存檔
    file_path = f"transcripts/{title}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {original_title}\n\n")
        f.write(f"> 收聽連結: {audio_url}\n\n")
        f.write(result["text"])
    
    print(f"完成！已生成: {file_path}")
    
    # 清理檔案
    if os.path.exists("latest_audio.mp3"):
        os.remove("latest_audio.mp3")

if __name__ == "__main__":
    run()
