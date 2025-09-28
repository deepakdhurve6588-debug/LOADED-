import asyncio
import json
import os
from playwright.async_api import async_playwright

# ------------------ Config ------------------
APPSTATE_FILE = "appstate.json"
USER_FILE = "replied_users.json"
MESSAGE_FILE = "messages.txt"
DELAY_BETWEEN_MESSAGES = 3  # seconds
CHECK_INTERVAL = 10  # seconds
# -------------------------------------------

class MessengerBot:
    def __init__(self):
        self.replied_users = self.load_replied_users()

    # -------- User Tracking --------
    def load_replied_users(self):
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        return set()

    def save_replied_users(self):
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(list(self.replied_users), f)

    def has_replied(self, user_id):
        return user_id in self.replied_users

    def mark_replied(self, user_id):
        self.replied_users.add(user_id)
        self.save_replied_users()

    # -------- Messages --------
    def read_messages(self):
        if not os.path.exists(MESSAGE_FILE):
            print(f"❌ Message file '{MESSAGE_FILE}' not found!")
            return []
        with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
            messages = [line.strip() for line in f if line.strip()]
        return messages

    # -------- Bot Loop --------
    async def run(self):
        messages = self.read_messages()
        if not messages:
            print("❌ No messages to send!")
            return

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=APPSTATE_FILE if os.path.exists(APPSTATE_FILE) else None
            )
            page = await context.new_page()

            await page.goto("https://www.messenger.com", timeout=60000)
            await page.wait_for_timeout(5000)

            # Save AppState if missing
            if not os.path.exists(APPSTATE_FILE):
                await context.storage_state(path=APPSTATE_FILE)
                print("💾 AppState saved! You can now use hosting without credentials.")

            while True:
                try:
                    # Find unread chats
                    unread_chats = await page.query_selector_all("//li//div[contains(@class,'unread')]")
                    if unread_chats:
                        print(f"📩 Found {len(unread_chats)} unread chats")
                        for chat in unread_chats:
                            await chat.click()
                            await page.wait_for_timeout(3000)

                            # Get user ID from URL
                            current_url = page.url
                            if "t/" in current_url:
                                user_id = current_url.split("t/")[-1].split("?")[0]
                            else:
                                user_id = "unknown"

                            if self.has_replied(user_id):
                                print(f"⏩ Already replied to {user_id}")
                                continue

                            # Send messages
                            msg_box = await page.wait_for_selector("div[role='textbox']")
                            for i, message in enumerate(messages, 1):
                                await msg_box.fill(message)
                                await msg_box.press("Enter")
                                print(f"✅ Sent message {i}/{len(messages)} to {user_id}")
                                if i < len(messages):
                                    await page.wait_for_timeout(DELAY_BETWEEN_MESSAGES * 1000)

                            self.mark_replied(user_id)
                            await page.wait_for_timeout(2000)
                    else:
                        print("⏳ No new messages")

                    await page.wait_for_timeout(CHECK_INTERVAL * 1000)

                except Exception as e:
                    print(f"❌ Error in loop: {e}")
                    await page.wait_for_timeout(10000)


# ------------------ Run Bot ------------------
if __name__ == "__main__":
    print("⚠️ WARNING: Automating Facebook Messenger may violate Terms of Service!")

    bot = MessengerBot()
    asyncio.run(bot.run())
