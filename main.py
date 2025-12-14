import os
import asyncio
import random
import json # JSON handling ke liye
from pyrogram import Client
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, PleaseWaitFewMinutes
from flask import Flask
from threading import Thread

# === RENDER CONFIGURATION ===
API_ID = 31908861
API_HASH = "db7b4118965e302e60cf66cc89570166"

TG_SESSION = os.environ.get("TG_SESSION")
# Hum IG_SETTINGS use karenge, IG_SESSION_ID nahi (safer for Render)
IG_SETTINGS_JSON = os.environ.get("IG_SETTINGS") 

BOT_INFO_1 = "@CYBERINFOXXXBOT"  
BOT_INFO_2 = "@TrueCalleRobot"     
BOT_ACTION = "@Lucixarp_bot"       
# =====================

# === WEB SERVER FOR UPTIMER (RENDER) ===
app_web = Flask(__name__)
@app_web.route('/')
def home():
    # Health check ke liye
    return "Bot is Running on Render!"
def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)
def keep_alive():
    t = Thread(target=run_web)
    t.start()
# ==============================================

def patch_instagrapi():
    try:
        from instagrapi.types import User
        User.model_config['extra'] = 'ignore'
    except Exception:
        pass
patch_instagrapi()

print("💀 Starting RENDER MASTER BOT...")

# === GLOBAL CLIENTS (Initial Placeholder) ===
# Clients ko main() ke andar initialize kiya jayega for stability
ig = InstaClient()

# Helper Functions (Needs app_client passed)
# (get_info_from_bot aur trigger_action_bot mein 'app_client' argument add kar diya gaya hai)

# ... (Insert Helper Functions 1 & 2 from previous working code) ...
# NOTE: Main un helper functions ko yahan copy-paste nahi kar raha hu taki code lamba na ho.
# Tu pichle reply se un dono functions ko wapas yahan daal dena.

# --- Helper Functions are here (assuming you pasted them) ---
async def get_info_from_bot(app_client, target_bot, query):
    try:
        sent_msg = await app_client.send_message(target_bot, query)
        await asyncio.sleep(2)
        
        for i in range(8): 
            await asyncio.sleep(1) 
            async for message in app_client.get_chat_history(target_bot, limit=1):
                if message.id > sent_msg.id:
                    raw_text = message.text or "📷 File Received"
                    if target_bot == BOT_INFO_1:
                        marker = "📞Telephone:"
                        if marker in raw_text:
                            return raw_text[raw_text.find(marker):]
                    return raw_text
        return f"⚠️ {target_bot} Slow."
    except Exception as e:
        return f"Error: {e}"

async def trigger_action_bot(app_client, target_bot, phone_10_digit):
    print(f"   💣 Triggering Action on {target_bot}...")
    try:
        sent_start = await app_client.send_message(target_bot, "/start")
        await asyncio.sleep(2) 
        
        button_clicked = False
        async for message in app_client.get_chat_history(target_bot, limit=1):
            if message.id > sent_start.id and message.reply_markup:
                if hasattr(message.reply_markup, 'keyboard'):
                    for row in message.reply_markup.keyboard:
                        for btn in row:
                            if btn.startswith("💣B") or btn.startswith("💣 B"):
                                print(f"      🔘 Clicking: {btn}")
                                await app_client.send_message(target_bot, btn)
                                button_clicked = True
                                break
                        if button_clicked: break
                
                if not button_clicked and hasattr(message.reply_markup, 'inline_keyboard'):
                    for row in message.reply_markup.inline_keyboard:
                        for btn in row:
                            if btn.text.startswith("💣B") or btn.text.startswith("💣 B"):
                                print(f"      🔘 Clicking Inline: {btn.text}")
                                await app_client.request_callback_answer(
                                    chat_id=message.chat.id,
                                    message_id=message.id,
                                    callback_data=btn.callback_data
                                )
                                button_clicked = True
                                break
                        if button_clicked: break
        
        if not button_clicked:
            print("      ❌ Button nahi mila '💣B' wala.")
            return False

        await asyncio.sleep(2)
        print(f"      🚀 Sending Target: {phone_10_digit}")
        await app_client.send_message(target_bot, phone_10_digit)
        return True

    except Exception as e:
        print(f"      ❌ Action Fail: {e}")
        return False
# --------------------------------------------------------------------------

def check_instagram_logic():
    # ... (Same logic as before) ...
    try:
        threads = ig.direct_threads(amount=1)
        if not threads: return None
        thread = threads[0]
        
        if thread.messages[0].user_id == ig.user_id: return None
        
        target_msg = None
        for msg in thread.messages[:5]:
            if msg.user_id == ig.user_id: continue 
            if msg.item_type != 'text': continue 
            if msg.id in PROCESSED_IDS: break 
            target_msg = msg
            break 
        
        if not target_msg: return None
        PROCESSED_IDS.add(target_msg.id)
        
        raw_text = target_msg.text.strip()
        clean_digits = "".join(filter(str.isdigit, raw_text))
        
        print(f"\n📩 Msg: {raw_text}")

        if len(clean_digits) >= 10:
            last_10 = clean_digits[-10:]
            final_full = "+91" + last_10
            
            if raw_text.lower().startswith("!b"):
                return {
                    "mode": "ACTION",
                    "user_id": target_msg.user_id,
                    "phone": last_10 
                }
            else:
                return {
                    "mode": "INFO",
                    "user_id": target_msg.user_id,
                    "phone": final_full 
                }
        return None

    except (ClientError, PleaseWaitFewMinutes) as e:
        print(f"\n🚨 INSTAGRAM LIMIT: {e}")
        return "COOL_DOWN"
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None

# === MAIN FUNCTION FOR RENDER ===
async def main():
    if not IG_SETTINGS_JSON or not TG_SESSION:
        print("❌ Secrets Missing! IG_SETTINGS aur TG_SESSION zaroori hain.")
        return

    # 1. Instagram Login (Using IG_SETTINGS JSON)
    print("🔵 Logging in Instagram (Persistent Mode)...")
    try:
        ig_settings = json.loads(IG_SETTINGS_JSON)
        ig.set_settings(ig_settings)
        # Session ID se login, settings se nahi
        ig.login_by_sessionid(ig_settings.get('sessionid')) 
        print("✅ Instagram Login Success!")
    except Exception as e:
        print(f"❌ Instagram Fail: Check IG_SETTINGS JSON: {e}")
        return

    # 2. Telegram Login (Deep Fix Mode)
    print("🔵 Logging in Telegram...")
    try:
        app = Client(
            "fresh_bot_client", 
            api_id=API_ID, 
            api_hash=API_HASH, 
            session_string=TG_SESSION, 
            in_memory=True
        )
        await app.start()
        print("✅ Telegram Login Success!")
    except Exception as e:
        print(f"❌ Telegram Fail (Session Error): {e}")
        return
    
    # Ignore Old Messages on Startup
    try:
        threads = ig.direct_threads(amount=3)
        if threads:
            for thread in threads:
                if thread.messages: PROCESSED_IDS.add(thread.messages[0].id)
    except: pass
    
    print("✅ All Systems Online & Ready for Render!")

    # MAIN LOOP
    while True:
        try:
            data = await asyncio.to_thread(check_instagram_logic)
            
            if data == "COOL_DOWN":
                print("⚠️ Rate Limit. Sleeping 2 mins...")
                await asyncio.sleep(120)
                continue
            
            if data and isinstance(data, dict):
                
                if data['mode'] == "ACTION":
                    print("⚙️ Mode: ACTION")
                    await trigger_action_bot(app, BOT_ACTION, data['phone'])
                    try:
                        ig.direct_send("💀 started baby girl", user_ids=[data['user_id']])
                    except: pass

                elif data['mode'] == "INFO":
                    print("⚙️ Mode: INFO")
                    info1 = await get_info_from_bot(app, BOT_INFO_1, data['phone'])
                    await asyncio.sleep(2)
                    info2 = await get_info_from_bot(app, BOT_INFO_2, data['phone'])
                    
                    final_reply = (
                        f"🤖 **Cyber Info:**\n{info1}\n\n"
                        f"➖➖➖➖➖➖➖\n\n"
                        f"🕵️ **TrueCaller:**\n{info2}"
                    )
                    try:
                        ig.direct_send(final_reply, user_ids=[data['user_id']])
                    except: pass

            print(f"💤 Waiting 15s...", end="\r")
            await asyncio.sleep(15)

        except Exception as e:
            print(f"\n⚠️ Critical Error: {e}")
            await asyncio.sleep(15)

if __name__ == "__main__":
    # Web server start karo for uptime monitoring
    keep_alive() 
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"☠️ Program Crashed: {e}")
