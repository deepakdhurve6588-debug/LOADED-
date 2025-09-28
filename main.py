import asyncio
import os
from playwright.async_api import async_playwright

APPSTATE_FILE = "appstate.json"
DELAY_BETWEEN_MESSAGES = 2  # seconds

async def send_message_to_uid(uid, messages):
    if not os.path.exists(APPSTATE_FILE):
        print("❌ appstate.json missing! Pehle local machine pe login karke bana lo.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=APPSTATE_FILE)
        page = await context.new_page()

        msg_url = f"https://www.messenger.com/t/{uid}"
        await page.goto(msg_url, timeout=60000)
        await page.wait_for_timeout(4000)  # Wait for load

        for i, message in enumerate(messages, 1):
            try:
                msg_box = await page.wait_for_selector("div[role='textbox']", timeout=10000)
                await msg_box.fill(message)
                await msg_box.press("Enter")
                print(f"✅ Sent message {i}/{len(messages)} to UID {uid}")
                await page.wait_for_timeout(DELAY_BETWEEN_MESSAGES * 1000)
            except Exception as e:
                print(f"❌ Error sending message {i}: {e}")

        await browser.close()

def read_messages_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Messages file {file_path} not found!")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    print("⚠️ Reminder: Facebook automation may violate Terms of Service. Use responsibly!")

    UID = "PUT_TARGET_UID_HERE"  # Yahan target user ka Facebook UID daalein

    messages = read_messages_from_file("messages.txt") or ["नमस्ते!"]

    asyncio.run(send_message_to_uid(UID, messages))
