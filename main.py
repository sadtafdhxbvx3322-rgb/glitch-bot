import os
import asyncio
import random
import json
from pyrogram import Client
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, PleaseWaitFewMinutes
from flask import Flask
from threading import Thread

# === CONFIGURATION ===
API_ID = 31908861
API_HASH = "db7b4118965e302e60cf66cc89570166"

TG_SESSION = os.environ.get("TG_SESSION")
IG_SESSION_ID = os.environ.get("IG_SESSION_ID")
IG_SETTINGS_JSON = os.environ.get("IG_SETTINGS") 

# 👇 BOT SETUP
BOT_INFO_1 = "@CYBERINFOXXXBOT"  
BOT_INFO_2 = "@TrueCalleRobot"     
BOT_ACTION = "@Lucixarp_bot"       
INSTA_DEBUG_USER = "@khooshzzz" # Debug message bhejne ke liye user
# =====================

# === WEB SERVER FOR UPTIMER (FLASK) ===
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot is Running on Render!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

def patch_instagrapi():
    try:
        from instagrapi.types import User
        User.model_config['extra'] = 'ignore'
    except Exception:
        pass
patch_instagrapi()

print("💀 Starting FINAL RENDER-OPTIMIZED BOT...")
patch_instagrapi()

# === GLOBAL CLIENTS ===
ig = InstaClient()
PROCESSED_IDS = set()

# Device Masking
ig.set_device({
    "app_version": "269.0.0.18.75",
    "android_version": 29,
    "android_release": "10.0",
    "dpi": "480dpi",
    "resolution": "1080x2340",
    "manufacturer": "Samsung",
    "device": "SM-S918B",
    "model": "Galaxy S23 Ultra",
    "cpu": "exynos990",
    "version_code": "314665256"
})

# === HELPER 1: INFO BOT ===
async def get_info_from_bot(app_client, target_bot, query):
    print(f"   ✈️ [{target_bot}] Sending Query: {query}")
    try:
        sent_msg = await app_client.send_message(target_bot, query)
        await asyncio.sleep(2)
        print(f"   ⏳ [{target_bot}] Waiting for reply...")
        
        for i in range(8): 
            await asyncio.sleep(1) 
            async for message in app_client.get_chat_history(target_bot, limit=1):
                if message.id > sent_msg.id:
                    print(f"   ✅ [{target_bot}] Reply received.")
                    raw_text = message.text or "📷 File Received"
                    if target_bot == BOT_INFO_1:
                        marker = "📞Telephone:"
                        if marker in raw_text:
                            return raw_text[raw_text.find(marker):]
                    return raw_text
        return f"⚠️ {target_bot} Slow."
    except Exception as e:
        print(f"   ❌ [{target_bot}] Error: {e}")
        return f"Error: {e}"

# === HELPER 2: ACTION BOT ===
async def trigger_action_bot(app_client, target_bot, phone_10_digit):
    print(f"   💣 Triggering Action on {target_bot}...")
    try:
        # Step 1: Send /start
        sent_start = await app_client.send_message(target_bot, "/start")
        print(f"      Sent /start. Waiting for menu...")
        await asyncio.sleep(2) 
        
        # Step 2: Click Button '💣B'
        button_clicked = False
        async for message in app_client.get_chat_history(target_bot, limit=1):
            if message.id > sent_start.id and message.reply_markup:
                # Logic to find and click button... (same as before)
                if hasattr(message.reply_markup, 'keyboard'):
                    for row in message.reply_markup.keyboard:
                        for btn in row:
                            if btn.startswith("💣B") or btn.startswith("💣 B"):
                                print(f"      🔘 Clicking Button: {btn}")
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
            print("      ❌ Button nahi mila '💣B' wala. Skipping number send.")
            return False

        # Step 3: Send Number
        await asyncio.sleep(2)
        print(f"      🚀 Sending Target Number: {phone_10_digit}")
        await app_client.send_message(target_bot, phone_10_digit)
        
        # Wait for final action acknowledgment (optional, but good for stability)
        await asyncio.sleep(3) 
        
        print("      ✅ Action Triggered and Number Sent.")
        return True

    except Exception as e:
        print(f"      ❌ Action Fail: {e}")
        return False

# === INSTAGRAM LOGIC ===
def check_instagram_logic():
    print("⏳ Waiting for messages on IG...")
    try:
        threads = ig.direct_threads(amount=1)
        if not threads: return None
        thread = threads[0]
        
        if thread.messages[0].user_id == ig.user_id: 
            print("   ✋ Last message Bot ka tha. Ignoring.")
            return None
        
        target_msg = None
        for msg in thread.messages[:5]:
            if msg.user_id == ig.user_id: continue 
            if msg.item_type != 'text': continue 
            if msg.id in PROCESSED_IDS: break 
            target_msg = msg
            break 
        
        if not target_msg: 
            print("   💤 No new unread messages found.")
            return None
        
        PROCESSED_IDS.add(target_msg.id)
        
        raw_text = target_msg.text.strip()
        clean_digits = "".join(filter(str.isdigit, raw_text))
        
        print(f"📩 Got message: '{raw_text}'")
        print(f"   Verifying if its number (Last 10 digits)...")

        if len(clean_digits) >= 10:
            last_10 = clean_digits[-10:]
            final_full = "+91" + last_10
            print(f"   ✅ Detected Number: {final_full}")
            
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
        print("   ❌ Number format not found (Too short). Ignoring.")
        return None

    except (ClientError, PleaseWaitFewMinutes) as e:
        print(f"\n🚨 INSTAGRAM LIMIT: {e}")
        return "COOL_DOWN"
    except Exception as e:
        print(f"⚠️ Error in IG check: {e}")
        return None

# === CORE ASYNC BOT LOOP ===
async def main_bot_loop(app):
    # Ignore Old Messages on Startup
    try:
        threads = ig.direct_threads(amount=3)
        if threads:
            for thread in threads:
                if thread.messages: PROCESSED_IDS.add(thread.messages[0].id)
        print(f"   [System] Ignored {len(PROCESSED_IDS)} old messages on startup.")
    except: pass
    
    print("✅ All Systems Online & Ready for Action!")

    # MAIN LOOP
    while True:
        try:
            data = await asyncio.to_thread(check_instagram_logic)
            
            if data == "COOL_DOWN":
                print("⚠️ Rate Limit. Sleeping 2 mins...")
                await asyncio.sleep(120)
                continue
            
            if data and isinstance(data, dict):
                
                # MODE 1: ACTION (!b)
                if data['mode'] == "ACTION":
                    print("--- ⚙️ MODE: ACTION (!b) ---")
                    await trigger_action_bot(app, BOT_ACTION, data['phone'])
                    
                    try:
                        ig.direct_send("💀 started baby girl", user_ids=[data['user_id']])
                        print("<<< 📤 Sending on IG: 'started baby girl'")
                        print("--- ✅ ACTION CYCLE COMPLETE ---")
                    except: pass

                # MODE 2: INFO (Normal)
                elif data['mode'] == "INFO":
                    print("--- ⚙️ MODE: INFO (Normal Number) ---")
                    
                    # Bot 1
                    info1 = await get_info_from_bot(app, BOT_INFO_1, data['phone'])
                    await asyncio.sleep(2)
                    
                    # Bot 2
                    info2 = await get_info_from_bot(app, BOT_INFO_2, data['phone'])
                    
                    final_reply = (
                        f"🤖 **Cyber Info:**\n{info1}\n\n"
                        f"➖➖➖➖➖➖➖\n\n"
                        f"🕵️ **TrueCaller:**\n{info2}"
                    )
                    
                    try:
                        ig.direct_send(final_reply, user_ids=[data['user_id']])
                        print("<<< 📤 Sending on IG: Combined Info.")
                        print("--- ✅ INFO CYCLE COMPLETE ---")
                    except: pass

            print(f"💤 Waiting 15s...", end="\r")
            await asyncio.sleep(15)

        except Exception as e:
            print(f"\n⚠️ Critical Error: {e}")
            await asyncio.sleep(15)

# === MAIN STARTUP FUNCTION (Handles Clients and Async Loop) ===
async def setup_and_start_bot():
    if not IG_SESSION_ID and not IG_SETTINGS_JSON:
        print("❌ INSTAGRAM Secret Missing!")
        return
    if not TG_SESSION:
        print("❌ TELEGRAM Secret Missing!")
        return

    # 1. Instagram Login (Debug 1)
    print("🔵 Logging in Instagram...")
    try:
        if IG_SETTINGS_JSON:
            ig_settings = json.loads(IG_SETTINGS_JSON)
            ig.set_settings(ig_settings)
            ig.login_by_sessionid(ig_settings.get('sessionid')) 
        else:
            ig.login_by_sessionid(IG_SESSION_ID)
            
        ig.direct_send("✅ Bot Live!", user_ids=[ig.user_id])
        await ig.direct_send("✅ Bot Live!", user_ids=[INSTA_DEBUG_USER])
        print(f"✅ Instagram Login Successful! Debug message sent to {INSTA_DEBUG_USER}")
    except Exception as e:
        print(f"❌ Instagram Login Fail: {e}")
        return

    # 2. Telegram Login (Debug 2)
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
        await app.send_message("me", "✅ **Telegram Login Successful!** Bot is now live.")
        print("✅ Telegram Login Successful! Live message sent to Saved Messages.")
    except Exception as e:
        print(f"❌ Telegram Fail: {e} (This is a Session String error!)")
        return
    
    # Start the main bot loop
    await main_bot_loop(app)

# === ENTRY POINT ===
def start_bot_in_background():
    # This runs the asynchronous bot setup in the background
    asyncio.run(setup_and_start_bot())

if __name__ == "__main__":
    # 1. Start Flask web server in a separate thread for Uptimer/Render
    t_web = Thread(target=run_web)
    t_web.start()
    print("🌐 Web server started (PORT 8080)")

    # 2. Start the main bot logic in a separate thread
    t_bot = Thread(target=start_bot_in_background)
    t_bot.start()
    print("🤖 Bot logic started in background thread.")
