import os
import random
from typing import List, Dict, Any
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# ---------------------- داده‌ها ----------------------
FACTS: List[str] = [
    "🌍 بدن انسان حدود ۶۰٪ از آب تشکیل شده.",
    "🦉 جغدها نمی‌توانند چشم‌هایشان را حرکت بدهند!",
    "⚡ مغز انسان حدود ۲۰ وات انرژی مصرف می‌کند."
]

WALLPAPERS: List[str] = [
    "https://picsum.photos/600/400?random=1",
    "https://picsum.photos/600/400?random=2",
    "https://picsum.photos/600/400?random=3",
    "https://picsum.photos/600/400?random=4"
]

ADMIN_ID = 8465015824  # 👈 آیدی عددی خودت رو اینجا بذار

# ---------------------- هندلرها ----------------------
def main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        ["📘 دانستنی", "🖼 والپیپر"],
        ["💬 درد دل ناشناس"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "سلام! من ربات تلگرام هستم 🤖\nیکی از گزینه‌های زیر رو انتخاب کن:",
        reply_markup=main_keyboard()
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()
    user_data: Dict[str, Any] = context.user_data

    if user_data.get("confess_mode"):
        confessions: List[str] = context.application.chat_data.setdefault("confessions", [])
        confessions.append(text)
        user_data["confess_mode"] = False
        await update.message.reply_text("✅ حرفت ذخیره شد و ناشناس باقی می‌مونه.")
        return

    if text == "📘 دانستنی":
        await update.message.reply_text(random.choice(FACTS))
    elif text == "🖼 والپیپر":
        await update.message.reply_photo(random.choice(WALLPAPERS))
    elif text == "💬 درد دل ناشناس":
        user_data["confess_mode"] = True
        await update.message.reply_text("می‌تونی هر چی می‌خوای ناشناس بگی. فقط بنویس و بفرست...")
    else:
        await update.message.reply_text("❓ دستور یا گزینه‌ی نامعتبر.", reply_markup=main_keyboard())

async def get_confess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔️ دسترسی نداری.")
        return

    confessions: List[str] = context.application.chat_data.get("confessions", [])
    if confessions:
        msg = "\n\n".join(confessions)
        await update.message.reply_text("📜 درد دل‌های ناشناس:\n\n" + msg)
    else:
        await update.message.reply_text("هیچ درد دلی ثبت نشده.")

# ---------------------- اجرای برنامه ----------------------
def get_token() -> str:
    return "8389152306:AAEUyzWV0pUxlADNHxokQAggIerWYyN7t70"  # 👈 اینجا توکن رباتت رو بذار

def main() -> None:
    token = get_token()
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getconfess", get_confess))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Bot is running. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()