import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ============================================================
# 👇👇👇 YAHAN APNA BOT TOKEN DAALEIN (BotFather se milega) 👇👇👇
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")

# ============================================================
# 👇👇👇 YAHAN APNI TELEGRAM USER ID DAALEIN 👇👇👇
# Apni ID pata karne ke liye @userinfobot ko message karein
# ============================================================
ADMIN_IDS = [123456789]  # <-- apni ID yahan daalein, comma se aur bhi add kar sakte hain

# ============================================================
# 👇👇👇 TRIGGER WORDS (customer ke message par REPLY/SWIPE karke yeh bhejna hai) 👇👇👇
# Chota-bada (case) koi farak nahi padta
# ============================================================
TRIGGER_ON = "auto mood on"
TRIGGER_OFF = "auto mood off"

# ============================================================
# 👇👇👇 YAHAN APNA CUSTOM AUTO-REPLY MESSAGE LIKHEIN 👇👇👇
# Isi message se customer ko reply jayega jab tak aap OFF na karein
# ============================================================
AUTO_REPLY_MESSAGE = """
Namaste! 🙏 Dhanyawad hamein message karne ke liye.

Hum abhi busy hain, jaldi hi aapko reply karenge.
Business hours: 10 AM - 7 PM

Aapka query note kar liya gaya hai.
"""

# Kis-kis customer ke liye auto-reply abhi ON hai (memory mein store, restart par reset ho jayega)
active_customers = set()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! Yeh business auto-reply bot hai.\n\n"
        "Kisi customer ke message par REPLY karke (swipe karke) likhein:\n"
        f"'{TRIGGER_ON}' — us customer ke liye auto-reply chalu karne ke liye\n"
        f"'{TRIGGER_OFF}' — us customer ke liye auto-reply band karne ke liye"
    )


async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jab ADMIN kisi customer ke message par reply/swipe karke trigger word bhejta hai"""
    msg = update.message
    text = (msg.text or "").strip().lower()

    # Yeh message kisi doosre message ka REPLY hona chahiye (swipe se hi aata hai)
    if not msg.reply_to_message:
        return

    target_user = msg.reply_to_message.from_user
    if target_user is None:
        return

    target_id = target_user.id

    if text == TRIGGER_ON:
        active_customers.add(target_id)
        await msg.reply_text(
            f"✅ Auto-reply ON kar diya gaya hai for {target_user.first_name} (ID: {target_id})"
        )
        logger.info(f"Admin turned auto-reply ON for customer {target_id}")

    elif text == TRIGGER_OFF:
        active_customers.discard(target_id)
        await msg.reply_text(
            f"🛑 Auto-reply OFF kar diya gaya hai for {target_user.first_name} (ID: {target_id})"
        )
        logger.info(f"Admin turned auto-reply OFF for customer {target_id}")


async def handle_customer_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Customer ka message aane par check karta hai ki uske liye auto-reply ON hai ya nahi"""
    user_id = update.effective_user.id

    if user_id in active_customers:
        await update.message.reply_text(AUTO_REPLY_MESSAGE)
        logger.info(f"Auto-replied to customer {user_id}")


async def route_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sabhi text messages yahan aate hain — decide karta hai admin ka hai ya customer ka"""
    user_id = update.effective_user.id

    if is_admin(user_id):
        # Agar yeh reply hai to trigger check karo, warna kuch mat karo
        await handle_admin_message(update, context)
    else:
        await handle_customer_message(update, context)


def main():
    if BOT_TOKEN == "PUT_YOUR_TOKEN_HERE":
        raise RuntimeError("Please set BOT_TOKEN environment variable or edit bot.py")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_message))

    logger.info("Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
