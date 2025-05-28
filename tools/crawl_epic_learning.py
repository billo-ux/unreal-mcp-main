import os, re, json, time, requests, logging
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from youtube_transcript_api import YouTubeTranscriptApi
from playwright.sync_api import sync_playwright

CACHE_DIR = Path('cache')
RAW_DIR = CACHE_DIR / 'raw'
CONSUMED_FILE = CACHE_DIR / 'consumed_sources.json'
BASE_URL = 'https://dev.epicgames.com/community/unreal-engine/learning'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'OptanonAlertBoxClosed=2024-07-08T12:37:14.822Z; _tald=a39220fa-2f55-4b35-993b-5a377159c749; _epicSID=6846e31bbbaf49a29983b4b7c71c3c41; cf_clearance=M4yeRZ2eRdCgoGcQw_OwYPYNJzhcr3Tt_Iabr.S2ef0-1748451580-1.2.1.1-AUhf8M39EThH9yaFy6QR..h3zKsdd2x_zSNwTSJDXYjsnIoYHIETzE8IaGHWyKS4eRW2MaXSK7tjbL9AP7Eo1CEHfpqpcftfdyUgnjdZzAZBZv0dMEBZxk1qdgdpHVZsVhy.o9AfBvlCbQGJsJ__8VpmyPzmt0zrlv_2ForCHiIVVbppKgtYy8.3ZS7XmeYjYC9bJth1VsDhwK.xes_VM0jwY6.BTxXx2rDG6l1orHFb.D8fD3pKnZMnjyalw6_1IdIJAG29BtCMLUj33dCkkyxx_D4X939pApVIebNbVAoZuXxwAlied2_knDdQj0Dj0yNM9jqJfOWGwkZaEldJmEVSOV2CnwYoFeJ2LG06EX8; PRIVATE-CSRF-TOKEN=1ETUC4H%2FCFeBgManyV1jVJWrIFUpIA00XBeZ8ce5SnU%3D; OptanonConsent=isIABGlobal=false&datestamp=Wed+May+28+2025+19%3A59%3A40+GMT%2B0300+(Eastern+European+Summer+Time)&version=6.7.0&hosts=&consentId=fe697318-4be1-4075-80cc-bd056146ab2e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A0&geolocation=GR%3B&AwaitingReconsent=false; OptanonConsent=isIABGlobal=false&datestamp=Wed+May+28+2025+19%3A59%3A40+GMT%2B0300+(Eastern+European+Summer+Time)&version=6.7.0&hosts=&consentId=fe697318-4be1-4075-80cc-bd056146ab2e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=GR%3B&AwaitingReconsent=false; EpicOptanonConsent=isIABGlobal=false&datestamp=Wed+May+28+2025+19%3A59%3A40+GMT%2B0300+(Eastern+European+Summer+Time)&version=6.7.0&hosts=&consentId=fe697318-4be1-4075-80cc-bd056146ab2e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=GR%3B&AwaitingReconsent=false; __cf_bm=8vrgnKtOTnZsfWrvw2GM3.Xbio.wzcUnANG_wJnQKM8-1748454242-1.0.1.1-pEMZVfanlul12NSMA331ReisicZQpuHWmLsLGa8dhHSkj3hc8BH9i82P82oL9l1I0f2Z5DteMraaRH0JanPj_oPv6wCoAXZLF9RTbdBdPfs'
}

logging.basicConfig(level=logging.INFO)
RAW_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

try:
    with open(CONSUMED_FILE, 'r', encoding='utf-8') as f:
        consumed = json.load(f)
except Exception:
    consumed = {}

def get_soup(url, screenshot_path=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        print('If there is a security check, please complete it in the browser window.')
        input('Press Enter here after the page is fully loaded and you see the content...')
        if screenshot_path:
            page.screenshot(path=screenshot_path)
        html = page.content()
        browser.close()
        return BeautifulSoup(html, 'lxml')

def get_course_links(page):
    url = BASE_URL if page == 1 else f"{BASE_URL}/page/{page}"
    screenshot_path = f"cache/raw/page_{page}.png" if page == 1 else None
    soup = get_soup(url, screenshot_path=screenshot_path)
    cards = soup.select('a.card')
    logging.info(f"[DEBUG] Page {page}: Found {len(cards)} course cards.")
    for c in cards:
        logging.info(f"[DEBUG] Card href: {c.get('href')}")
    return [c['href'] for c in cards if c.get('href')]

def extract_youtube_id(soup):
    yt = soup.find('iframe', src=re.compile('youtube.com/embed/([\w-]+)'))
    if yt:
        m = re.search(r'/embed/([\w-]+)', yt['src'])
        return m.group(1) if m else None
    return None

def extract_vtt_url(soup):
    track = soup.find('track', kind='subtitles', src=True)
    return track['src'] if track else None

def extract_article_text(soup):
    art = soup.find('article')
    return art.get_text(separator='\n').strip() if art else ''

def fetch_transcript_youtube(video_id):
    try:
        tx = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return '\n'.join([x['text'] for x in tx])
    except Exception as e:
        logging.warning(f"YouTube transcript failed: {e}")
        return ''

def fetch_transcript_vtt(vtt_url):
    try:
        r = requests.get(vtt_url, headers=HEADERS)
        r.raise_for_status()
        cues = re.findall(r'\d+:\d+:\d+\.\d+ --> .*?\n(.*?)\n', r.text, re.DOTALL)
        return '\n'.join([c.strip() for c in cues if c.strip()])
    except Exception as e:
        logging.warning(f"VTT transcript failed: {e}")
        return ''

def process_course(url):
    soup = get_soup(url)
    yt_id = extract_youtube_id(soup)
    vtt_url = extract_vtt_url(soup)
    slug = url.rstrip('/').split('/')[-1]
    source_id = f"yt-{yt_id}" if yt_id else slug
    if source_id in consumed:
        logging.info(f"Skipping {source_id} (already consumed)")
        return
    text = ''
    if yt_id:
        text = fetch_transcript_youtube(yt_id)
    if not text and vtt_url:
        text = fetch_transcript_vtt(vtt_url)
    if not text:
        text = extract_article_text(soup)
    if not text:
        logging.warning(f"No transcript/text found for {url}")
        return
    out_path = RAW_DIR / f"{source_id}.txt"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)
    consumed[source_id] = datetime.now(timezone.utc).isoformat()
    logging.info(f"Saved {source_id} ({len(text)} chars)")

def main():
    page = 1
    seen = set()
    while True:
        links = get_course_links(page)
        if not links:
            break
        for rel in links:
            url = rel if rel.startswith('http') else f"https://dev.epicgames.com{rel}"
            if url in seen:
                continue
            seen.add(url)
            try:
                process_course(url)
            except Exception as e:
                logging.error(f"Failed to process {url}: {e}")
        page += 1
    with open(CONSUMED_FILE, 'w', encoding='utf-8') as f:
        json.dump(consumed, f, indent=2)
    logging.info("Done.")

if __name__ == '__main__':
    main() 