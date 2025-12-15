import os
import asyncio
import random
from pyrogram import Client
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, PleaseWaitFewMinutes

# === CONFIGURATION ===
API_ID = 31908861
API_HASH = "db7b4118965e302e60cf66cc89570166"

# === 🔥 HARDCODED SESSIONS (LATEST VALID SESSION) 🔥 ===
# AGAR NAYA SESSION BANAYA HAI TOH ISSE UPDATE KARNA!
TG_SESSION_HARDCODE = "BQHm4_0Awq5IC-ruOoCimNRqipYhDY-l9kYXJMfUvw5iSeENxgogXTuqYVbAARubM_fuYpgv_AJg6nW9hCk5a69XLRiEM1qUIMj8dck_UBtQFFRP5YdR6CyApBznFcjmL-jbdTB3xDHgq8qE81VufDGGEWlmFbua5geJo_1KHqYoXRaP5LICwQGRci8evZ5cBW3vucdZyhLCzJ-NB6tNP7ZWBScG0YtGHpC1t6gcxqb5v5JZtMH4UUaqDu1-8TkLOeb7kWpxIsSJUCnIJcxXgGZigUZ7ncg_JudPRGEXUDIfRkNszuxFf_f44LlkWHP3CHUWm-NGnaxQA-0BLx_3gtaD6tx23gAAAAHylqcSAA"
IG_SESSION_ID_HARDCODE = "75136570684%3Af6PP2JHwpjctRF%3A22%3AAYhcx-naKgkUhqsz2R6v89yWhTFOZvaDtGbdCunwMw" 
# =======================================================

# 👇 BOT GROUPS
BOT_INFO_LIST = ["@CYBERINFOXXXBOT", "@TrueCalleRobot"]
BOT_ACTION_LIST = ["@crazy_tools_bot", "@Lucixarp_bot", "@DadeisBack_bot"]

# === INITIALIZATION (Syntax Fixed) ===
def patch_instagrapi():
    try:
        from instagrapi.types import User
        User.model_config['extra'] = 'ignore' 
    except Exception:
        pass
patch_instagrapi()

print("💀 Starting FINAL MASTER BOT (New Project Ready)...")

# === CLIENT INITIALIZATION ===
app = Client(
    "railway_new_client", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=TG_SESSION_HARDCODE, 
    in_memory=True
)

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

# === HELPER 1: INFO BOT (FINAL SPAM FIX LOGIC) ===
async def get_info_from_bot(app_client, target_bot, query):
    print(f"   ✈️ [{target_bot}] Sending Query: {query}")
    try:
        sent_msg = await app_client.send_message(target_bot, query)
        await asyncio.sleep(2)
        print(f"   ⏳ [{target_bot}] Waiting for reply...")
        
        try:
            target_user = await app_client.get_users(target_bot)
            target_id = target_user.id
        except Exception:
            target_id = None 

        for i in range(8): 
            await asyncio.sleep(1) 
            async for message in app_client.get_chat_history(target_bot, limit=1):
                is_from_target_bot = (target_id is not None and message.from_user.id == target_id)
                is_not_self_message = (message.from_user.id != app_client.me.id)
                is_new_message = (message.id > sent_msg.id)
                
                if is_new_message and is_not_self_message and (target_id is None or is_from_target_bot):
                    
                    print(f"   ✅ [{target_bot}] Reply received.")
                    raw_text = message.text or "📷 File Received"
                    if target_bot == "@CYBERINFOXXXBOT":
                        marker = "📞Telephone:"
                        if marker in raw_text:
                            return raw_text[raw_text.find(marker):]
                    return raw_text
        return f"⚠️ {target_bot} Slow/No Reply."
    except Exception as e:
        print(f"   ❌ [{target_bot}] Error: {e}")
        return f"Error: {e}"

# === HELPER 2: ACTION BOT ===
async def trigger_action_bot(app_client, target_bot, phone_10_digit):
    print(f"   💣 Triggering Action on {target_bot}...")
    try:
        sent_start = await app_client.send_message(target_bot, "/start")
        print(f"      Sent /start. Waiting for menu...")
        await asyncio.sleep(3) 
        
        button_clicked = False
        async for message in app_client.get_chat_history(target_bot, limit=1):
            if message.id > sent_start.id and message.reply_markup:
                
                if hasattr(message.reply_markup, 'keyboard'):
                    for row in message.reply_markup.keyboard:
                        for btn in row:
                            if "Start Bombing" in btn or btn.startswith("💣B") or btn.startswith("💣 B"):
                                print(f"      🔘 Clicking Button: {btn}")
                                await app_client.send_message(target_bot, btn)
                                button_clicked = True
                                break
                        if button_clicked: break
                
                if not button_clicked and hasattr(message.reply_markup, 'inline_keyboard'):
                    for row in message.reply_markup.inline_keyboard:
                        for btn in row:
                            if "Start Bombing" in btn.text or btn.text.startswith("💣B") or btn.text.startswith("💣 B"):
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
            print("      ❌ Action Button ('Start Bombing' or '💣B') nahi mila.")
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

# === MAIN BOT LOOP ===
async def main():
    if not IG_SESSION_ID_HARDCODE:
        print("❌ Instagram Session Hardcode Missing!")
        return

    # 1. Instagram Login
    print("🔵 Logging in Instagram...")
    try:
        ig.login_by_sessionid(IG_SESSION_ID_HARDCODE)
        print("✅ Instagram Login Success!")
    except Exception as e:
        print(f"❌ Instagram Fail: {e}")
        return

    # 2. Telegram Login
    print("🔵 Logging in Telegram...")
    try:
        await app.start()
        print("✅ Telegram Login Success!")
    except Exception as e:
        print(f"❌ Telegram Fail: {e}")
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
                    
                    ig.direct_send("💀 Bombing started on 3 bots...", user_ids=[data['user_id']])
                    
                    # ACTION on all 3 bots
                    for bot_username in BOT_ACTION_LIST:
                        await trigger_action_bot(app, bot_username, data['phone'])
                        await asyncio.sleep(1) 
                    
                    print("<<< 📤 Sending on IG: Bombing initiated.")
                    print("--- ✅ ACTION CYCLE COMPLETE ---")

                elif data['mode'] == "INFO":
                    print("--- ⚙️ MODE: INFO (Normal Number) ---")
                    
                    info_parts = []
                    
                    # INFO from all 2 bots
                    for bot_username in BOT_INFO_LIST:
                        info_result = await get_info_from_bot(app, bot_username, data['phone'])
                        info_parts.append(f"🤖 **Info from {bot_username}:**\n{info_result}")
                        await asyncio.sleep(1)
                    
                    final_reply = "\n\n➖➖➖➖➖➖➖\n\n".join(info_parts)
                    
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
