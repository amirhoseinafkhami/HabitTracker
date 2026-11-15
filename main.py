import os
import sqlite3
import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler, MessageHandler, filters
)

# بارگذاری توکن از فایل .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# ==================== بخش دیتابیس ====================
def init_db():
    """ساخت جداول دیتابیس در صورت عدم وجود"""
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    # جدول کاربران
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    # جدول عادت‌ها
    c.execute('''CREATE TABLE IF NOT EXISTS habits (
                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER, 
                    name TEXT)''')
    # جدول ثبت روزانه (لاگ)
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    habit_id INTEGER, 
                    date TEXT, 
                    status INTEGER)''')
    conn.commit()
    conn.close()

# اجرای تابع ساخت دیتابیس هنگام شروع
init_db()

# ==================== حالت‌های مکالمه ====================
ASK_HABIT_NAME = 1

# ==================== دستورات ربات ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(
        "سلام! به ربات ردیاب عادت خوش آمدید. 🌟\n\n"
        "دستورات موجود:\n"
        "🔹 /addhabit : افزودن عادت جدید\n"
        "🔹 /today : مشاهده و ثبت عادت‌های امروز"
    )

async def add_habit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً نام عادت جدید را وارد کنید (مثلاً: ورزش، مطالعه، زبان انگلیسی):")
    return ASK_HABIT_NAME

async def add_habit_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    habit_name = update.message.text
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute("INSERT INTO habits (user_id, name) VALUES (?, ?)", (user_id, habit_name))
    conn.commit()
    conn.close()
    await update.message.reply_text(f"عادت «{habit_name}» با موفقیت اضافه شد! ✅")
    return ConversationHandler.END

async def today_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    today = datetime.date.today().isoformat()
    
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''SELECT h.habit_id, h.name, l.status FROM habits h 
                 LEFT JOIN logs l ON h.habit_id = l.habit_id AND l.date = ?
                 WHERE h.user_id = ?''', (today, user_id))
    habits = c.fetchall()
    conn.close()

    if not habits:
        await update.message.reply_text("شما هنوز هیچ عادتی تعریف نکرده‌اید. از /addhabit استفاده کنید.")
        return

    keyboard = []
    for habit_id, name, status in habits:
        status_icon = "✅" if status == 1 else "❌"
        keyboard.append([InlineKeyboardButton(f"{status_icon} {name}", callback_data=f"toggle_{habit_id}_{today}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("وضعیت عادت‌های امروز شما:", reply_markup=reply_markup)

# ==================== مدیریت کلیک روی دکمه‌ها ====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data.startswith("toggle_"):
        _, habit_id, date = data.split("_")
        habit_id = int(habit_id)
        
        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute("SELECT status FROM logs WHERE habit_id = ? AND date = ?", (habit_id, date))
        row = c.fetchone()
        
        # تغییر وضعیت (اگر نبود ثبت کن، اگر بود برعکسش کن)
        if row is None:
            c.execute("INSERT INTO logs (habit_id, date, status) VALUES (?, ?, 1)", (habit_id, date))
        else:
            new_status = 0 if row[0] == 1 else 1
            c.execute("UPDATE logs SET status = ? WHERE habit_id = ? AND date = ?", (new_status, habit_id, date))
        
        conn.commit()
        
        # به‌روزرسانی کیبورد
        user_id = query.from_user.id
        c.execute('''SELECT h.habit_id, h.name, l.status FROM habits h 
                     LEFT JOIN logs l ON h.habit_id = l.habit_id AND l.date = ?
                     WHERE h.user_id = ?''', (date, user_id))
        habits = c.fetchall()
        conn.close()

        keyboard = []
        for hid, name, status in habits:
            status_icon = "✅" if status == 1 else "❌"
            keyboard.append([InlineKeyboardButton(f"{status_icon} {name}", callback_data=f"toggle_{hid}_{date}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)

# ==================== اجرای اصلی برنامه ====================
def main():
    if not TOKEN:
        print("خطا: توکن ربات پیدا نشد! فایل .env را بررسی کنید.")
        return

    application = Application.builder().token(TOKEN).build()

    # مکالمه برای گرفتن نام عادت جدید
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addhabit", add_habit_start)],
        states={
            ASK_HABIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_habit_save)],
        },
        fallbacks=[]
    )

    # اتصال هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("today", today_habits))
    application.add_handler(CallbackQueryHandler(button_callback))

    print("ربات در حال اجراست...")
    application.run_polling()

if __name__ == '__main__':
    main()