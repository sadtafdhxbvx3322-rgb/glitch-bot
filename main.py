import os
import asyncio
import random
from pyrogram import Client
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, PleaseWaitFewMinutes

# === CONFIGURATION ===
API_ID = 31908861
API_HASH = "db7b4118965e302e60cf66cc89570166"

# === 🔥 HARDCODED SESSIONS 🔥 ===
TG_SESSION_HARDCODE = "BQHm4_0Ae4rPe42j9ql0j8mEsmHWUovyr4Ezp3v--IEGSB2H-LXd5jMQcye2UPDFIRtHj4g8fn9mK3DPTGxlke5ioHYxvWNbwSO5d-jw9wu5lebh3JffA6Cy4Lq-H5A5sGw_mtKgsVr-e7wJkpfTJrJ5CcoTIS8xtjG4h5XnRkPMmhzBnmIObbR5_gZtUsZP4RLukw7-hUHaXT_Dx1tcWhKABe8rdZusau1XobP4ef0uHL3bfkiCR4tka8-VfkxYtO-ViSgvHB3Sd5io1XprsKye2afe3h-esm7D749vhC4dc6J7yk-3e1JLv1JzdRl4RItEN1IzEdg36w5HK9ffTlTDGd4nqQAAAAHylqcSAA"
IG_SESSION_ID_HARDCODE = "1904077537%3ACwsjF0H1m75TBF%3A7%3AAYg6T-U_5_nZ4c8NXnwRfOLRyWzE4g6WJVpCY_BAaw" 
# =======================================================

# 👇 BOT SETUP
BOT_INFO_1 = "@CYBERINFOXXXBOT"  
BOT_INFO_2 = "@TrueCalleRobot"     
BOT_ACTION = "@Lucixarp_bot"       
INSTA_DEBUG_USER = "@khooshzzz"
# =====================

def patch_instagrapi():
    try:
        from instagrapi.types import User
        User.model_config['extra'] = 'ignore'
    except Exception:
        pass
patch_instagrapi()

print("💀 Starting RAILWAY FINAL FIX BOT (Clean Separation)...")

# === INSTAGRAM CLIENT (Global) ===
ig = InstaClient()
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

PROCESSED_IDS = set()

# === TELEGRAM HELPERS (Need to be defined before main) ===

async def get_info_from_bot(app_client, target_bot, query):
    print(f"   ✈️ [{target_bot}] Sending Query: {query}")
    # ... (rest of the logic) ...
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

async def trigger_action_bot(app_client, target_bot, phone_10_digit):
    print(f"   💣 Triggering Action on {target_bot}...")
    # ... (rest of the logic) ...
    try:
        sent_start = await app_client.send_message(target_bot, "/start")
        print(f"      Sent /start. Waiting for menu...")
        await asyncio.sleep(2) 
        
        button_clicked = False
        async for message in app_client.get_chat_history(target_bot, limit=1):
            if message.id > sent_start.id and message.reply_markup:
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

        await asyncio.sleep(2)
        print(f"      🚀 Sending Target Number: {phone_10_digit}")
        await app_client.send_message(target_bot, phone_10_digit)
        await asyncio.sleep(3) 
        
        print("      ✅ Action Triggered and Number Sent.")
        return True

    except Exception as e:
        print(f"      ❌ Action Fail: {e}")
        return False


def check_instagram_logic():
    print("⏳ Waiting for messages on IG...")
    # ... (rest of the logic) ...
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

# === MAIN BOT LOOP (Telegram Client inside) ===
async def main():
    if not IG_SESSION_ID_HARDCODE:
        print("❌ Instagram Session Hardcode Missing!")
        return

    # 1. Instagram Login (First Step)
    print("🔵 Logging in Instagram...")
    try:
        ig.login_by_sessionid(IG_SESSION_ID_HARDCODE)
        ig.direct_send("✅ Bot Live!", user_ids=[ig.user_id])
        print("✅ Instagram Login Success!")
    except Exception as e:
        # Agar yahan error aaya, toh IG session galat hai
        print(f"❌ Instagram Fail: {e}. IG Session check karo!")
        return

    # 2. Telegram Client Initialization (After IG)
    print("🔵 Logging in Telegram...")
    try:
        # Naya Client object yahan banaya
        app = Client(
            "railway_fix_client", 
            api_id=API_ID, 
            api_hash=API_HASH, 
            session_string=TG_SESSION_HARDCODE, 
            in_memory=True
        )
        await app.start()
        await app.send_message("me", "✅ **Telegram Login Successful!** Bot is now live.")
        print("✅ Telegram Login Success!")
    except Exception as e:
        # Agar yahan error aaya, toh TG session galat hai
        print(f"❌ Telegram Fail: {e}. TG Session check karo!")
        return

    try:
        threads = ig.direct_threads(amount=3)
        if threads:
            for thread in threads:
                if thread.messages: PROCESSED_IDS.add(thread.messages[0].id)
        print(f"   [System] Ignored {len(PROCESSED_IDS)} old messages on startup.")
    except: pass
    
    print("✅ All Systems Online & Ready!")

    while True:
        try:
            data = await asyncio.to_thread(check_instagram_logic)
            
            if data == "COOL_DOWN":
                print("⚠️ Rate Limit. Sleeping 2 mins...")
                await asyncio.sleep(120)
                continue
            
            if data and isinstance(data, dict):
                
                if data['mode'] == "ACTION":
                    print("--- ⚙️ MODE: ACTION (!b) ---")
                    await trigger_action_bot(app, BOT_ACTION, data['phone'])
                    
                    try:
                        ig.direct_send("💀 started baby girl", user_ids=[data['user_id']])
                        print("<<< 📤 Sending on IG: 'started baby girl'")
                        print("--- ✅ ACTION CYCLE COMPLETE ---")
                    except: pass

                elif data['mode'] == "INFO":
                    print("--- ⚙️ MODE: INFO (Normal Number) ---")
                    
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
                        print("<<< 📤 Sending on IG: Combined Info.")
                        print("--- ✅ INFO CYCLE COMPLETE ---")
                    except: pass

            print(f"💤 Waiting 15s...", end="\r")
            await asyncio.sleep(15)

        except Exception as e:
            print(f"\n⚠️ Critical Error: {e}")
            await asyncio.sleep(15)

if __name__ == "__main__":
    try:
        asyncio.run(main()) 
    except Exception as e:
        print(f"☠️ Program Crashed: {e}")
