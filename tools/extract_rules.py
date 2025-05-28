import os, json, hashlib, openai, yaml
from pathlib import Path
from datetime import datetime
import tiktoken

CACHE_DIR = Path('cache')
RAW_DIR = CACHE_DIR / 'raw'
RULES_FILE = CACHE_DIR / 'rules.json'
CONSUMED_FILE = CACHE_DIR / 'consumed_sources.json'
CONFIG_FILE = Path('config/guideline_ingest.yaml')

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)

openai.api_key = os.getenv('OPENAI_API_KEY')

enc = tiktoken.get_encoding('cl100k_base')

def chunk_text(text, max_tokens):
    words = text.split()
    chunks, chunk = [], []
    for w in words:
        chunk.append(w)
        if len(enc.encode(' '.join(chunk))) > max_tokens:
            chunks.append(' '.join(chunk))
            chunk = []
    if chunk:
        chunks.append(' '.join(chunk))
    return chunks

def prompt_rules(chunk):
    prompt = f"""Extract Unreal-Engine best-practice rules.\n\n• Each rule ≤ {cfg['rule_len']} characters.\n• Prefix each rule with one category from: {', '.join(cfg['categories'])}.\n\nText:\n{chunk}\n"""
    resp = openai.ChatCompletion.create(
        model=cfg['model'],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=cfg['rule_len'] * 10,
        temperature=0.2,
    )
    return [l.lstrip('•').strip() for l in resp['choices'][0]['message']['content'].split('\n') if l.strip()]

def main():
    with open(CONSUMED_FILE, 'r', encoding='utf-8') as f:
        consumed = json.load(f)
    rules = {}
    for txt in RAW_DIR.glob('*.txt'):
        source_id = txt.stem
        mtime = datetime.utcfromtimestamp(txt.stat().st_mtime).isoformat()
        if source_id in consumed and mtime <= consumed[source_id]:
            continue
        with open(txt, 'r', encoding='utf-8') as f:
            text = f.read()
        for chunk in chunk_text(text, cfg['chunk_tokens']):
            for rule in prompt_rules(chunk):
                h = hashlib.md5(rule.lower().encode()).hexdigest()
                rules[h] = rule
    with open(RULES_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(rules.values()), f, indent=2)

if __name__ == '__main__':
    main() 