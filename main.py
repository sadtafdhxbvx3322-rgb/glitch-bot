import os
import json
import asyncio
import time
import glob
from threading import Thread
from instagrapi import Client
from telethon import TelegramClient
from telethon.sessions import StringSession
from groq import Groq
import yt_dlp

# === 1. LOAD SECRETS FROM RAILWAY ===
TG_APP_ID = int(os.environ["TG_APP_ID"])
TG_APP_HASH = os.environ["TG_APP_HASH"]
TG_SESSION = os.environ["TG_SESSION_STR"]
IG_USER = os.environ["IG_USER"]
IG_PASS = os.environ["IG_PASS"]
IG_SESSION = os.environ["IG_SESSION_STR"]
# Agar Groq key nahi hai to niche wali line delete kar dena
GROQ_KEY = os.environ.get("GROQ_API_KEY", "none") 

# Target Bot (Jisse number nikalna hai)
TRUECALLER_BOT_USER = "@TrueCaller_Bot" 

# === 2. SETUP CLIENTS ===
# Setup AI
groq = None
if GROQ_KEY != "none":
    groq = Groq(api_key=GROQ_KEY)

# Setup Telegram (Async)
tg_client = TelegramClient(StringSession(TG_SESSION), TG_APP_ID, TG_APP_HASH)

# Setup Instagram (Sync)
ig_client = Client()

def login_instagram():
    """Login using the SAVED SESSION to avoid Ban"""
    print("🟠 Logging into Instagram...")
    try:
        # Load the JSON string you generated
        settings = json.loads(IG_SESSION)
        ig_client.set_settings(settings)
        ig_client.login(IG_USER, IG_PASS)
        print("✅ Logged in via Session String! (Safe Mode)")
    except Exception as e:
        print(f"⚠️ Session Login Failed: {e}")
        print("Trying raw password login...")
        ig_client.login(IG_USER, IG_PASS)

# === 3. FEATURES ===

def download_song(query):
    """Downloads song via yt-dlp"""
    print(f"🎵 Searching: {query}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        filename = f"downloads/{info['entries'][0]['id']}.m4a"
    return filename

def get_ai_reply(text):
    """Chat with AI"""
    if not groq: return "AI disabled. Add API Key."
    try:
        resp = groq.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a Gen Z homie. Reply short, funny, use slang (fr, ngl, cooked)."},
                {"role": "user", "content": text}
            ],
            model="llama3-8b-8192"
        )
        return resp.choices[0].message.content
    except:
        return "Brain not working rn 💀"

async def get_truecaller_data(number):
    """Ask Telegram Bot for Info"""
    async with tg_client:
        print(f"🕵️‍♂️ Asking Truecaller bot about: {number}")
        await tg_client.send_message(TRUECALLER_BOT_USER, number)
        await asyncio.sleep(5) # Wait for reply
        msgs = await tg_client.get_messages(TRUECALLER_BOT_USER, limit=1)
        return msgs[0].text

# === 4. MAIN LOOP ===
def start_bot():
    login_instagram()
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print("🚀 BOT IS ONLINE AND READY!")
    
    while True:
        try:
            # Check unread messages
            threads = ig_client.direct_threads(amount=5, selected_filter="unread")
            
            for thread in threads:
                msg = thread.messages[0]
                text = msg.text
                user_pk = thread.users[0].pk
                
                # Skip own messages
                if str(msg.user_id) == str(ig_client.user_id):
                    continue

                print(f"📩 Msg from {thread.users[0].username}: {text}")
                
                # --- COMMANDS ---

                # A. SONG REQUEST (!play fein)
                if text.lower().startswith("!play "):
                    song_name = text[6:].strip()
                    ig_client.direct_send("Wait, cooking that up... 🎧", thread_ids=[thread.id])
                    try:
                        path = download_song(song_name)
                        ig_client.direct_send_voice(thread.id, path)
                        os.remove(path) # Delete file after sending
                    except Exception as e:
                        ig_client.direct_send("Song nahi mila bro ❌", thread_ids=[thread.id])

                # B. TRUECALLER (10 Digits)
                elif text.isdigit() and len(text) >= 10:
                    ig_client.direct_send("Scanning dark web... 🕵️‍♂️", thread_ids=[thread.id])
                    
                    # Run Async Telegram Task
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    info = loop.run_until_complete(get_truecaller_data(text))
                    
                    ig_client.direct_send(f"📂 REPORT:\n{info}", thread_ids=[thread.id])

                # C. AI CHAT
                elif "?" in text or "bot" in text.lower():
                    reply = get_ai_reply(text)
                    ig_client.direct_send(reply, thread_ids=[thread.id])

            time.sleep(15) # Wait 15s before checking again to avoid ban

        except Exception as e:
            print(f"⚠️ Error in loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    start_bot()
