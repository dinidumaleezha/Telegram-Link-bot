import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = "https://www.capcut.com//template-detail//"

def check_link(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except:
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # Validate ID
    if not user_input.isdigit():
        await update.message.reply_text(
            "❌ Invalid input.\nPlease send numbers only."
        )
        return

    link = BASE_URL + user_input
    is_working = check_link(link)

    if is_working:
        keyboard = [
            [InlineKeyboardButton("🔗 Open Link", url=link)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"✅ Link is working.\n\n{link}",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            f"❌ Link is not working or failed to load.\n\n{link}"
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
