#!/usr/bin/env python3
import requests, json
from datetime import datetime, timezone

SYMBOLS = {
    'krw':   'KRW=X',
    'wti':   'CL=F',
    'kospi': '^KS11',
    'gold':  'XAUUSD=X',
    'brent': 'BZ=F',
    'sp500': '^GSPC',
}
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def fetch_yahoo(symbol):
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=3mo&interval=1d'
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    res = r.json()['chart']['result'][0]
    current = res['meta']['regularMarketPrice']
    ts = res.get('timestamp', [])
    closes = res['indicators']['quote'][0].get('close', [])
    history = [
        {'date': datetime.utcfromtimestamp(t).strftime('%Y-%m-%d'), 'close': c}
        for t, c in zip(ts, closes) if c is not None
    ]
    return {'current': current, 'history': history}

out = {'updatedAt': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
for key, symbol in SYMBOLS.items():
    try:
        out[key] = fetch_yahoo(symbol)
        print(f'{key}: {out[key]["current"]} ({len(out[key]["history"])} days)')
    except Exception as e:
        print(f'{key}: FAILED — {e}')
        out[key] = None

with open('data.json', 'w') as f:
    json.dump(out, f)
print('data.json updated at', out['updatedAt'])
