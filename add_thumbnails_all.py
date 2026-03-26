"""
articles.jsonの全記事にOGP画像URLを付与する（thumbnailなし記事のみ）
"""
import json
import urllib.request
import re
import sys

sys.stdout = __import__('io').TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INPUT = "C:/Users/moyam/OneDrive/ドキュメント/Obsidian保管庫/ai-navigator/articles.json"

def get_ogp_image(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as res:
            html = res.read().decode("utf-8", errors="ignore")
        m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html)
        return m.group(1) if m else None
    except Exception:
        return None

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

articles = data["articles"]
targets = [a for a in articles if not a.get("thumbnail") and a.get("url", "").startswith("http")]

print(f"サムネなし記事: {len(targets)}件 -> OGP取得開始")
ok = 0
for i, a in enumerate(targets, 1):
    thumb = get_ogp_image(a["url"])
    if thumb:
        a["thumbnail"] = thumb
        ok += 1
    if i % 50 == 0:
        print(f"  {i}/{len(targets)}件処理中... (取得成功: {ok}件)")

with open(INPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"完了: {ok}/{len(targets)}件取得成功")
