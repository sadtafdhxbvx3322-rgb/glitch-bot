import os
import asyncio
import random
import logging
from pyrogram import Client
from pyrogram.errors import AuthKeyInvalid, AuthKeyUnregistered
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, PleaseWaitFewMinutes

# === LOGGING SETUP (FIXED) ===
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)  # <--- YEH LINE MISSING THI
# ===================================

# === CONFIGURATION ===
API_ID = 35892347
# ... (Rest of the code remains the same)

API_HASH = "24f0ab191c17d8a58f0ac1d85d99d0f1"

# === 🔥 HARDCODED SESSIONS (LATEST WORKING STRINGS) 🔥 ===
# Nayi, choti TG session string yahan daal di gayi hai.
TG_SESSION_HARDCODE = "BQIjrHsAAQ3dNrZmEuDaxpQW38fAt4vKFceM6zD7LH7ardO1XqX60cRbcFQVTjqfmdbnULLMaaCK1V_1__clCKa1tPPJQ4p2RhJouipUFuHwyzqfNKVYGylpyUXoiC3Sr8P5Yv8gGPKSgirzXvo_vctWzKAVYcL-GKis4ArsUNgKmO8DLYeImwHlj0s3s1NmGCGfT4hsFK2tGyyDoHTL2bh9XmsGFLOzNlIwHrWJ3lk7ts73gougN7syxxfclw0Aduf7Dx7pF5gw226Kk4C2ReOIPxndJJWkFNoPcmYuG4KyHM106_PGHVu48FbhqPCXit5Shbi4gqL3jCdgaTDpL6Hl60DqNgAAAAHfi28uAA"
IG_SESSION_ID_HARDCODE = "79571086246%3AeuyWvK0olWrlKS%3A16%3AAYhk_bxwsgEHbgZYjOMTftKo0jU_zRtMGVfrmKtJVw" 
# =======================================================

# ... (BOT GROUPS and patch_instagrapi remains same) ...

logger.info("💀 Starting FINAL MASTER BOT (Pyrogram 2.x Compatible)...")

# === CLIENT INITIALIZATION (PYROGRAM 2.x SYNTAX) ===
# Syntax is correct for Pyrogram 2.0.106
app = Client(
    "railway_final_client", 
    api_id=API_ID, 
    api_hash=API_HASH,
    session_string=TG_SESSION_HARDCODE,
    in_memory=True
)

ig = InstaClient()
# ... (Device Masking remains same) ...

PROCESSED_IDS = set()

# ... (HELPER 1: INFO BOT and HELPER 2: ACTION BOT remain same) ...

# === MAIN BOT LOOP (Connection Logic Fixed) ===
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

    # 2. Telegram Login (CRITICAL FIX APPLIED HERE)
    logger.info("🔵 Logging in Telegram...")
    try:
        # Pyrogram 2.x client start: Now testing the new short session string
        await app.start() 
        me = await app.get_me() # Connection test
        logger.info(f"✅ Telegram Login Success! Logged in as @{me.username}")
    
    except AuthKeyInvalid:
        logger.critical("❌ Telegram Login Failed: AUTH_KEY_INVALID (Session Expired). Please regenerate your session.")
        return
    except AuthKeyUnregistered:
        logger.critical("❌ Telegram Login Failed: AUTH_KEY_UNREGISTERED (Session Deleted). Please regenerate your session.")
        return
    except Exception as e:
        logger.critical(f"❌ Telegram Login Fail: Unhandled Error: {e}")
        return
    
    # ... (Rest of the main loop remains same) ...
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
