# 新聞雷達：抓取關鍵字的最新新聞，組成一則訊息，送到你的 LINE。

# 載入 Python 內建的模組，下面的程式會用到。
import json
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

# 你關注的主題。課堂上先用這個，最後一堂會換成你自己的。
KEYWORD = "颱風"

# 一則訊息最多列幾條新聞，減少訊息過多。
MAX_ITEMS = 5


# 組網址：把關鍵字接進 Google News 的 RSS 查詢網址（中文要先編碼）。
def make_feed_url(keyword):
    query = urllib.parse.quote(keyword)
    return (
        "https://news.google.com/rss/search?q=" + query
        + "&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    )


# 抓新聞：把 RSS 內容抓回來，整理成一筆一筆的新聞（標題與連結）。
def fetch_news(url):
    req = urllib.request.Request(url, headers={"User-Agent": "news-radar/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml_text = resp.read()
    root = ET.fromstring(xml_text)
    items = []
    for item in root.iter("item"):
        items.append({
            "title": item.findtext("title", ""),
            "link": item.findtext("link", ""),
        })
    return items


# 組訊息：把新聞清單組成一則通知訊息。
def build_message(keyword, items):
    picked = items[:MAX_ITEMS]
    lines = ["【新聞雷達】「" + keyword + "」有 " + str(len(picked)) + " 則新消息"]
    for item in picked:
        lines.append("・" + item["title"])
    return "\n".join(lines)


# 送通知：用 LINE 的 broadcast API，把訊息廣播給這個 bot 的所有好友。
def send_notification(message, token):
    body = json.dumps(
        {"messages": [{"type": "text", "text": message}]}
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/broadcast",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status


# 主流程：組網址、抓新聞、組訊息，最後送通知。
def main():
    url = make_feed_url(KEYWORD)
    items = fetch_news(url)
    if not items:
        print("這次沒有抓到任何新聞。")
        return
    message = build_message(KEYWORD, items)
    token = os.environ.get("LINE_TOKEN", "")
    if token == "":
        print("（還沒設定存取權杖，先把訊息印出來看看）")
        print(message)
        return
    send_notification(message, token)
    print("已送出通知。")


# 執行這個檔案時，從 main() 開始跑。
if __name__ == "__main__":
    main()
