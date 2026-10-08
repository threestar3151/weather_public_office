# 오늘의 유통 브리핑 (무료)

- 날씨: Open-Meteo (무료, API 키 없음) — 브라우저에서 직접 호출
- 뉴스: Google 뉴스 RSS — 하루 2번 자동 수집해 `data/news.js` 저장
- 호스팅: GitHub Pages (공개 저장소 무료)

## 내 PC에서 바로 보기
1. `python scripts/fetch_news.py` (뉴스 최신화, 파이썬만 있으면 됨)
2. `index.html` 더블클릭

## 인터넷에 올리기 (자동 갱신)
1. GitHub 가입 → New repository (Public)
2. 이 폴더의 파일 전체를 업로드 (`.github` 폴더 포함)
3. Settings → Pages → Branch: `main` / `(root)` → Save
4. Actions 탭 → update-news → Run workflow (첫 수집)
5. 이후 매일 06:00, 12:00에 자동 갱신 (GitHub 사정으로 몇 분~수십 분 늦을 수 있음)

## 고치는 곳
- 지역: `index.html` 의 `CITIES`
- 검색어: `scripts/fetch_news.py` 의 `SECTIONS`
- 갱신 시각: `.github/workflows/update-news.yml` 의 cron (UTC 기준, KST-9시간)
