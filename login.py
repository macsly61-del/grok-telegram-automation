import asyncio
import json
from playwright.async_api import async_playwright

async def save_session():
    async with async_playwright() as p:
        # Browser SICHTBAR öffnen
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Grok öffnen
        await page.goto('https://grok.com')
        
        print("=== Browser geöffnet! ===")
        print("1. Logge dich jetzt manuell bei Grok ein")
        print("2. Warte bis du im Chat bist")
        print("3. Drücke dann ENTER in diesem Terminal")
        
        input("Drücke ENTER wenn du eingeloggt bist...")
        
        # Session speichern
        cookies = await context.cookies()
        storage = await context.storage_state()
        
        with open('grok_session.json', 'w') as f:
            json.dump(storage, f)
        
        print("=== Session gespeichert in grok_session.json! ===")
        await browser.close()

asyncio.run(save_session())
