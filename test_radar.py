# radar.py 的自動化測試。用 uv run pytest 執行。

# 從 radar.py 載入這次要測試的兩個函式。
from radar import build_message, make_feed_url


# 驗網址：中文關鍵字有沒有被正確編碼進網址。
def test_網址包含編碼後的關鍵字():
    url = make_feed_url("颱風")
    assert "news.google.com" in url
    assert "%E9%A2%B1%E9%A2%A8" in url


# 驗訊息：組出來的訊息裡有沒有主題、標題與數量。
def test_訊息包含關鍵字與標題():
    items = [
        {"title": "測試新聞一", "link": "https://example.com/1"},
        {"title": "測試新聞二", "link": "https://example.com/2"},
    ]
    message = build_message("測試主題", items)
    assert "測試主題" in message
    assert "測試新聞一" in message
    assert "2 則" in message


# 驗上限：給十條新聞，訊息裡應該只出現五條。
def test_訊息最多只列五則():
    items = [
        {"title": "新聞" + str(n), "link": "https://example.com/" + str(n)}
        for n in range(1, 11)
    ]
    message = build_message("測試主題", items)
    assert "5 則" in message
    assert "新聞6" not in message
