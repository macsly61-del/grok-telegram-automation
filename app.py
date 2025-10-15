from flask import Flask, jsonify
import asyncio
from playwright.async_api import async_playwright
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "8376996434:AAG4f3djBHorRLSCaF2NIVoiV8lrwb7Ztak"
CHAT_ID = "5956127672"
GROK_URL = "https://grok.com/c/d53ee40b-cd9b-4850-9a7f-c72da1801bcf"
PROMPT = "flüstern? Alles was mit crypto pump zutun hat. Das leise flüstern, was man hört danach Ausschau halten. weltweit, was aktuell ist nicht von der vergangenheit kontrolliere datum Wallet-Bewegungen50k+ Follower, kleine Käufe. Nur echte. Antworte kurz: Asset, Zeit, Chance – oder 'Ruhe'."

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

async def run_grok():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
        page = await browser.new_page()
        
        # Stealth: User Agent manuell setzen
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        await page.goto(GROK_URL, wait_until='networkidle', timeout=60000)
        await asyncio.sleep(10)
        
        selector = 'div.response-content-markdown > p, div.response-content-markdown > strong'
        initial_count = await page.locator(selector).count()
        
        await page.fill('input[type="text"], textarea, div[role="textbox"]', PROMPT)
        await page.keyboard.press('Enter')
        
        response_text = ''
        for i in range(400):
            current_count = await page.locator(selector).count()
            if current_count > initial_count:
                text = await page.locator(selector).last.inner_text()
                if text and 'flüstern' not in text.lower():
                    response_text = text.strip()
                    break
            await asyncio.sleep(0.5)
        
        await browser.close()
        return response_text or 'Keine Antwort'

@app.route('/run', methods=['GET'])
def run():
    try:
        print("=== Starting Grok automation ===")
        result = asyncio.run(run_grok())
        print(f"=== Got result: {result} ===")
        send_telegram(f"🔔 Grok: {result}")
        return jsonify({"success": True, "response": result})
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"=== ERROR: {error_msg} ===")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": error_msg}), 500

@app.route('/')
def home():
    return "Grok Telegram Bot läuft!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
