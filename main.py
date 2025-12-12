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
from instagrapi.exceptions import ChallengeRequired, BadPassword, PleaseWaitException

# === 0. DEBUGGER (CONFIRMATION) ===
print("🔍 SYSTEM DIAGNOSTICS: Bot is launching...")

# === 1. CONFIGURATION (HARDCODED & ENVIRONMENT) ===
TG_APP_ID = 31908861
TG_APP_HASH = "db7b4118965e302e60cf66cc89570166"
TRUECALLER_BOT_USER = "@TrueCaller_Bot" # Change if different

# --- LOAD SECRETS FROM RAILWAY ---
TG_SESSION = os.environ.get("TG_SESSION_STR")
IG_USER = os.environ.get("IG_USER") # glitch.tools
IG_PASS = os.environ.get("IG_PASS") # Khush@123!!!!!!
IG_SESSION = os.environ.get("IG_SESSION_STR")
GROQ_KEY = os.environ.get("GROQ_API_KEY")

# === 2. SETUP CLIENTS ===
# Setup AI
groq = None
if GROQ_KEY:
    try:
        groq = Groq(api_key=GROQ_KEY)
    except:
        print("⚠️ Groq Key invalid.")

# Setup Telegram (Async)
tg_client = None
if TG_SESSION:
    try:
        tg_client = TelegramClient(StringSession(TG_SESSION), TG_APP_ID, TG_APP_HASH)
    except Exception as e:
        print(f"❌ Telegram Client Initialization Error: {e}")

# Setup Instagram (Sync)
ig_client = Client()

def login_instagram():
    """Login logic with detailed error handling."""
    print("🟠 Logging into Instagram...")
    if not IG_SESSION or not IG_USER or not IG_PASS:
        print("❌ CRITICAL: IG credentials missing from Railway Variables.")
        os._exit(1) # Fail fast

    # Attempt 1: Session Login
    try:
        print("DEBUG: Trying Session Login...")
        settings = json.loads(IG_SESSION)
        ig_client.set_settings(settings)
        ig_client.login(IG_USER, IG_PASS)
        print("✅ Logged in via Session String! (Safe Mode)")
        return
    except (ChallengeRequired, BadPassword, PleaseWaitException) as e:
        print(f"⚠️ Session Login Failed: {e}. Trying Password Fallback...")
    except Exception as e:
        print(f"⚠️ Generic Session Error: {e}. Trying Password Fallback...")

    # Attempt 2: Password Login
    try:
        ig_client.login(IG_USER, IG_PASS)
        print("✅ Logged in via Password")
    except ChallengeRequired as e:
        print("\n❌ CRITICAL ERROR: CHALLENGE REQUIRED")
        print("ACTION: Approve the login on your phone. Then redeploy.")
        os._exit(1) # Stop and wait for user action
    except BadPassword:
        print("❌ CRITICAL ERROR: BAD PASSWORD.")
        print("ACTION: Check IG_PASS in Railway Variables.")
        os._exit(1)
    except Exception as e2:
        print(f"❌ FINAL LOGIN FAILURE: {e2}")
        os._exit(1)

# === 3. FEATURES (Code from previous prompt) ===

# --- Copy/Paste the rest of the functions here ---
def download_song(query):
    # ... (rest of the download_song function)
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
    # ... (rest of the get_ai_reply function)
    if not groq: return "My brain is disconnected rn 💀"
    try:
        resp = groq.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a Gen Z homie. Reply short, funny, use slang."},
                {"role": "user", "content": text}
            ],
            model="llama3-8b-8192"
        )
        return resp.choices[0].message.content
    except:
        return "Brain not working rn 💀"

async def get_truecaller_data(number):
    # ... (rest of the get_truecaller_data function)
    if not tg_client: return "Telegram Bridge is Down ❌"
    async with tg_client:
        print(f"🕵️‍♂️ Asking Truecaller bot about: {number}")
        await tg_client.send_message(TRUECALLER_BOT_USER, number)
        await asyncio.sleep(5)
        msgs = await tg_client.get_messages(TRUECALLER_BOT_USER, limit=1)
        return msgs[0].text
# -----------------------------------------------

# === 4. MAIN LOOP ===
def start_bot():
    login_instagram()
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print("🚀 BOT IS STARTING LOOP...")
    
    while True:
        try:
            threads = ig_client.direct_threads(amount=5, selected_filter="unread")
            
            for thread in threads:
                msg = thread.messages[0]
                text = msg.text
                
                if str(msg.user_id) == str(ig_client.user_id): continue

                print(f"📩 Msg from {thread.users[0].username}: {text}")
                
                # --- COMMANDS ---

                # A. SONG REQUEST (!play fein)
                if text.lower().startswith("!play "):
                    song_name = text[6:].strip()
                    ig_client.direct_send("Wait, cooking that up... 🎧", thread_ids=[thread.id])
                    try:
                        path = download_song(song_name)
                        ig_client.direct_send_voice(thread.id, path)
                        os.remove(path)
                    except Exception as e:
                        print(f"Song Error: {e}")
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

            time.sleep(15)

        except Exception as e:
            print(f"⚠️ Error in loop: {e}")
            time.sleep(30)

if __name__ == "__main__":
    start_bot()
