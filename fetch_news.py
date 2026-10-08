"""구글 뉴스 RSS(무료, 키 불필요)에서 유통 관련 기사를 모아 data/news.js 로 저장합니다.
사용법:  python scripts/fetch_news.py
검색어는 아래 SECTIONS 만 고치면 됩니다.
"""
import json, re, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

KST = timezone(timedelta(hours=9))
MAX_ITEMS = 20

SECTIONS = [
    {"id": "law", "title": "법·제도", "queries": [
        "유통산업발전법", "가맹사업법", "대규모유통업법", "최저임금 편의점",
        "공정위 편의점", "담배사업법", "주 4.5일제 OR 노동법 유통",
    ]},
    {"id": "news", "title": "유통 뉴스", "queries": [
        "편의점", "유통업계", "GS25 OR CU OR 세븐일레븐", "프랜차이즈 가맹점주",
    ]},
]

def fetch(query, period):
    q = urllib.parse.quote(f"{query} when:{period}")
    url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            root = ET.fromstring(r.read())
    except Exception as e:
        print("실패:", query, e)
        return []
    out = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        src = (it.findtext("source") or "").strip()
        if src and title.endswith(" - " + src):
            title = title[: -len(src) - 3]
        try:
            pub = parsedate_to_datetime(it.findtext("pubDate")).astimezone(KST)
        except Exception:
            continue
        out.append({"title": title, "source": src,
                    "link": it.findtext("link") or "", "published": pub.isoformat()})
    return out

def collect(section):
    for period in ("1d", "3d"):          # 오늘 기사가 너무 적으면 3일로 넓힘
        seen, items = set(), []
        for q in section["queries"]:
            for it in fetch(q, period):
                key = re.sub(r"\W+", "", it["title"])[:30]
                if key and key not in seen:
                    seen.add(key)
                    items.append(it)
        if len(items) >= 5:
            break
    items.sort(key=lambda x: x["published"], reverse=True)
    return items[:MAX_ITEMS]

def main():
    data = {"updated": datetime.now(KST).isoformat(timespec="seconds"),
            "sections": [{"id": s["id"], "title": s["title"], "items": collect(s)} for s in SECTIONS]}
    out = Path(__file__).resolve().parent.parent / "data" / "news.js"
    out.write_text("window.NEWS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print("저장:", out, [len(s["items"]) for s in data["sections"]])

if __name__ == "__main__":
    main()
