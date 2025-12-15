import os
import asyncio
import random
import logging
from pyrogram import Client
from pyrogram.errors import AuthKeyInvalid, AuthKeyUnregistered
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, PleaseWaitFewMinutes

# === LOGGING SETUP ===
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
# ===================================

# === CONFIGURATION ===
API_ID = 35892347
API_HASH = "24f0ab191c17d8a58f0ac1d85d99d0f1"

# === 🔥 HARDCODED SESSIONS (LATEST STRING) 🔥 ===
# NOTE: Agar yeh string phir se 'unpack requires a buffer' error de, toh yeh string corrupt hai
# aur use dobara generate karna hi padega (Pyrogram 2.0.x se).
TG_SESSION_HARDCODE = "1BVtsOI0Bu6ihp5vZy7xwezfUeGWxsjxXVYN_6H4LA-SP1132JLTY2tAYzADXvqbkwLtWGNGwg5BUZx7O7bilrZkvvXd-5ldp-HQntVaHF0-bVUSHeUKArMHeR4gSZaa8ljlF82oScCqABEH1ZstuL8UQbqOtI1sWoy8-JbRJK03y8DOquPqjDyJsjMRU1LKTwPwpWKTrweSGeOdASEjPQihMFIDJokr1giSHmRhKkYMz99cRfz-AjbHymGZiS5gl5q6Pdl0oB0yIHMci35E0rmFxYYD53Z-u5STM9oIFWEFs35BVMXSoMGNv5NkNQOS1W2GlTBMmdf-XijvWLioDHKjKn2jRthA="
IG_SESSION_ID_HARDCODE = "78342326870%3AVVLrZpcWpSXlXN%3A20%3AAYjiEedYjjbaN06kwIhsfH5ejYHnWLOCJVh26Jp9rQ" 
# =======================================================

# 👇 BOT GROUPS
BOT_INFO_LIST = ["@CYBERINFOXXXBOT", "@TrueCalleRobot"] 
BOT_ACTION_LIST = ["@crazy_tools_bot", "@Lucixarp_bot", "@DadeisBack_bot"]

# === INITIALIZATION ===
def patch_instagrapi():
    try:
        from instagrapi.types import User
        User.model_config['extra'] = 'ignore' 
    except Exception:
        pass
patch_instagrapi()

logger.info("💀 Starting FINAL MASTER BOT (Pyrogram 2.x Compatible)...")

# === CLIENT INITIALIZATION (PYROGRAM 2.x SYNTAX) ===
# Pyrogram 2.x mein yeh arguments zaroori hain.
app = Client(
    "railway_final_client", 
    api_id=API_ID, 
    api_hash=API_HASH,
    session_string=TG_SESSION_HARDCODE, # 'session_string=' keyword zaroori hai
    in_memory=True                     # 'in_memory=' keyword zaroori hai
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

# === HELPER 1: INFO BOT (ULTIMATE SPAM FIX V3) ===
async def get_info_from_bot(app_client, target_bot, query):
    logger.debug(f"   ✈️ [{target_bot}] Sending Query: {query}")
    clean_query_number = "".join(filter(str.isdigit, query))[-10:]
    
    try:
        sent_msg = await app_client.send_message(target_bot, query)
        await asyncio.sleep(2)
        logger.debug(f"   ⏳ [{target_bot}] Waiting for reply (Sent ID: {sent_msg.id})...")
        
        try:
            target_user = await app_client.get_users(target_bot)
            target_id = target_user.id
        except Exception:
            target_id = None 

        for i in range(10): 
            await asyncio.sleep(1) 
            
            async for message in app_client.get_chat_history(target_bot, limit=1): 
                
                is_new_message = (message.id > sent_msg.id)
                is_from_target_bot = (target_id is not None and message.from_user.id == target_id)
                is_not_self_message = (message.from_user.id != app_client.me.id)
                
                is_content_relevant = False
                if message.text:
                    if clean_query_number in message.text.replace(' ', '').replace('+', ''):
                         is_content_relevant = True
                    elif target_bot == "@CYBERINFOXXXBOT" and "📞Telephone:" in message.text:
                         is_content_relevant = True

                if is_new_message and is_not_self_message and is_content_relevant and (target_id is None or is_from_target_bot):
                    
                    logger.debug(f"   ✅ [{target_bot}] Reply received & Content Matched.")
                    raw_text = message.text or "📷 File Received"
                    
                    if target_bot == "@CYBERINFOXXXBOT":
                        marker = "📞Telephone:"
                        if marker in raw_text:
                            return raw_text[raw_text.find(marker):]
                    return raw_text
        
        return f"⚠️ {target_bot} Slow/No Reply (Timeout)."
        
    except Exception as e:
        logger.error(f"   ❌ [{target_bot}] Error: {e}")
        return f"Error: {e}"

# === HELPER 2: ACTION BOT (3 Bots Working Logic) ===
async def trigger_action_bot(app_client, target_bot, phone_10_digit):
    logger.debug(f"   💣 Triggering Action on {target_bot}...")
    try:
        sent_start = await app_client.send_message(target_bot, "/start")
        await asyncio.sleep(5) 
        
        button_clicked = False
        async for message in app_client.get_chat_history(target_bot, limit=1):
            if message.id > sent_start.id and message.reply_markup:
                
                if hasattr(message.reply_markup, 'keyboard'):
                    for row in message.reply_markup.keyboard:
                        for btn in row:
                            if "Start Bombing" in btn or "Start bombing" in btn or btn.startswith("💣B") or btn.startswith("💣 B"):
                                logger.debug(f"      🔘 Clicking Keyboard Button: {btn}")
                                await app_client.send_message(target_bot, btn)
                                button_clicked = True
                                break
                        if button_clicked: break
                
                if not button_clicked and hasattr(message.reply_markup, 'inline_keyboard'):
                    for row in message.reply_markup.inline_keyboard:
                        for btn in row:
                            btn_text_lower = btn.text.lower()
                            if "start bombing" in btn_text_lower or btn_text_lower.startswith("💣b") or btn_text_lower.startswith("💣 b"):
                                logger.debug(f"      🔘 Clicking Inline Button: {btn.text}")
                                await app_client.request_callback_answer(
                                    chat_id=message.chat.id,
                                    message_id=message.id,
                                    callback_data=btn.callback_data
                                )
                                button_clicked = True
                                break
                        if button_clicked: break
        
        if not button_clicked:
            logger.debug("      ❌ Action Button ('Start Bombing' or '💣B') nahi mila. Skipping Number Send.")
            return False

        await asyncio.sleep(2) 
        logger.debug(f"      🚀 Sending Target Number: {phone_10_digit}")
        await app_client.send_message(target_bot, phone_10_digit)
        await asyncio.sleep(3) 
        
        logger.debug("      ✅ Action Triggered and Number Sent.")
        return True

    except Exception as e:
        logger.error(f"      ❌ Action Fail: {e}")
        return False

# === INSTAGRAM LOGIC (Anti-Spam Filter Active) ===
def check_instagram_logic():
    logger.debug("⏳ Waiting for messages on IG...")
    try:
        threads = ig.direct_threads(amount=1)
        if not threads: return None
        thread = threads[0]
        
        if thread.messages[0].user_id == ig.user_id: 
            logger.debug("   ✋ Last message Bot ka tha. Ignoring.")
            return None
        
        target_msg = None
        for msg in thread.messages[:5]:
            if msg.user_id == ig.user_id: continue 
            if msg.item_type != 'text': continue 
            if msg.id in PROCESSED_IDS: break 
            target_msg = msg
            break 
        
        if not target_msg: 
            logger.debug("   💤 No new unread messages found.")
            return None
        
        PROCESSED_IDS.add(target_msg.id)
        
        raw_text = target_msg.text.strip()
        
        # --- IGNORE SELF-GENERATED MESSAGES ---
        if raw_text.startswith("Error: Telegram says:") or raw_text.startswith("🤖 **Info from @"):
            logger.debug(f"   ⚠️ Ignoring self-generated Error/Info loop content: {raw_text[:30]}...")
            return None
        # ----------------------------------------
        
        clean_digits = "".join(filter(str.isdigit, raw_text))
        
        logger.info(f"📩 Got message: '{raw_text}'")

        if len(clean_digits) >= 10:
            last_10 = clean_digits[-10:]
            final_full = "+91" + last_10
            logger.info(f"   ✅ Detected Number: {final_full}")
            
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
        logger.debug("   ❌ Number format not found (Too short). Ignoring.")
        return None

    except (ClientError, PleaseWaitFewMinutes) as e:
        logger.warning(f"\n🚨 INSTAGRAM LIMIT: {e}")
        return "COOL_DOWN"
    except Exception as e:
        logger.error(f"⚠️ Error in IG check: {e}")
        return None

# === MAIN BOT LOOP ===
async def main():
    if not IG_SESSION_ID_HARDCODE:
        logger.error("❌ Instagram Session Hardcode Missing!")
        return

    # 1. Instagram Login
    logger.info("🔵 Logging in Instagram...")
    try:
        ig.login_by_sessionid(IG_SESSION_ID_HARDCODE)
        logger.info("✅ Instagram Login Success!")
    except Exception as e:
        logger.critical(f"❌ Instagram Fail: {e}")
        return

    # 2. Telegram Login 
    logger.info("🔵 Logging in Telegram...")
    try:
        await app.start()
        logger.info("✅ Telegram Login Success!")
    
    except AuthKeyInvalid:
        logger.critical("❌ Telegram Login Failed: AUTH_KEY_INVALID (Session Expired). Please regenerate your session.")
        return
    except AuthKeyUnregistered:
        logger.critical("❌ Telegram Login Failed: AUTH_KEY_UNREGISTERED (Session Deleted). Please regenerate your session.")
        return
    except Exception as e:
        logger.critical(f"❌ Telegram Login Fail: Unhandled Error: {e}")
        return
    
    try:
        threads = ig.direct_threads(amount=3)
        if threads:
            for thread in threads:
                if thread.messages: PROCESSED_IDS.add(thread.messages[0].id)
        logger.info(f"   [System] Ignored {len(PROCESSED_IDS)} old messages on startup.")
    except: pass
    
    logger.info("✅ All Systems Online & Ready!")

    while True:
        try:
            data = await asyncio.to_thread(check_instagram_logic)
            
            if data == "COOL_DOWN":
                logger.warning("⚠️ Rate Limit. Sleeping 2 mins...")
                await asyncio.sleep(120)
                continue
            
            if data and isinstance(data, dict):
                
                if data['mode'] == "ACTION":
                    logger.info("--- ⚙️ MODE: ACTION (!b) ---")
                    
                    ig.direct_send("💀 Bombing started on 3 bots...", user_ids=[data['user_id']])
                    
                    for bot_username in BOT_ACTION_LIST:
                        await trigger_action_bot(app, bot_username, data['phone'])
                        await asyncio.sleep(1) 
                    
                    logger.info("<<< 📤 Sending on IG: Bombing initiated.")
                    logger.info("--- ✅ ACTION CYCLE COMPLETE ---")

                elif data['mode'] == "INFO":
                    logger.info("--- ⚙️ MODE: INFO (Normal Number) ---")
                    
                    info_parts = []
                    
                    for bot_username in BOT_INFO_LIST:
                        info_result = await get_info_from_bot(app, bot_username, data['phone'])
                        info_parts.append(f"🤖 **Info from {bot_username}:**\n{info_result}")
                        await asyncio.sleep(1)
                    
                    final_reply = "\n\n➖➖➖➖➖➖➖\n\n".join(info_parts)
                    
                    try:
                        ig.direct_send(final_reply, user_ids=[data['user_id']])
                        logger.info("<<< 📤 Sending on IG: Combined Info.")
                        logger.info("--- ✅ INFO CYCLE COMPLETE ---")
                    except: pass

            logger.debug(f"💤 Waiting 15s...", end="\r")
            await asyncio.sleep(15)

        except Exception as e:
            logger.critical(f"\n⚠️ Critical Error in Main Loop: {e}")
            await asyncio.sleep(15)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"☠️ Program Crashed: {e}")
