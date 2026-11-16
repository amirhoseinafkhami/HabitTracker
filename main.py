import os
import sqlite3
import datetime
<<<<<<< HEAD
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
=======
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa
    ContextTypes, ConversationHandler, MessageHandler, filters
)

# بارگذاری توکن از فایل .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
<<<<<<< HEAD
PROXY = os.getenv("PROXY_URL")  # اختیاری، مثلا http://127.0.0.1:10809
=======
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa

# ==================== بخش دیتابیس ====================
def init_db():
    """ساخت جداول دیتابیس در صورت عدم وجود"""
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    # جدول کاربران
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    # جدول عادت‌ها
    c.execute('''CREATE TABLE IF NOT EXISTS habits (
<<<<<<< HEAD
                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT)''')
    # جدول ثبت روزانه (لاگ)
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER,
                    date TEXT,
                    status INTEGER)''')
    # جلوگیری از ثبت تکراری برای یک عادت در یک روز
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_log
                 ON logs(habit_id, date)''')
=======
                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER, 
                    name TEXT)''')
    # جدول ثبت روزانه (لاگ)
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    habit_id INTEGER, 
                    date TEXT, 
                    status INTEGER)''')
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa
    conn.commit()
    conn.close()

# اجرای تابع ساخت دیتابیس هنگام شروع
init_db()

# ==================== حالت‌های مکالمه ====================
ASK_HABIT_NAME = 1

<<<<<<< HEAD
# ==================== توابع کمکی ====================
def get_streak(habit_id):
    """تعداد روزهای متوالی انجام یک عادت"""
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute("SELECT date FROM logs WHERE habit_id=? AND status=1", (habit_id,))
    done = {datetime.date.fromisoformat(r[0]) for r in c.fetchall()}
    conn.close()

    day = datetime.date.today()
    if day not in done:  # اگر امروز هنوز انجام نشده، از دیروز بشمار
        day -= datetime.timedelta(days=1)
    streak = 0
    while day in done:
        streak += 1
        day -= datetime.timedelta(days=1)
    return streak


def build_today_view(user_id, date):
    """ساخت متن و دکمه‌های نمای امروز (برای /today و کلیک دکمه‌ها و یادآور)"""
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''SELECT h.habit_id, h.name, l.status FROM habits h
                 LEFT JOIN logs l ON h.habit_id = l.habit_id AND l.date = ?
                 WHERE h.user_id = ?''', (date, user_id))
=======
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
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa
    habits = c.fetchall()
    conn.close()

    if not habits:
<<<<<<< HEAD
        return "شما هنوز هیچ عادتی تعریف نکرده‌اید. از /addhabit استفاده کنید.", None

    done = sum(1 for _, _, s in habits if s == 1)
    total = len(habits)
    filled = round(10 * done / total)
    bar = "🟩" * filled + "⬜" * (10 - filled)

    if done == total:
        msg = "🎉 همه‌ی عادت‌ها انجام شد! عالی بودی!"
    elif done:
        msg = "💪 ادامه بده، نزدیکی!"
    else:
        msg = "🌅 روز جدید، شروع جدید!"

    text = f"📅 عادت‌های امروز\n\n{bar}  {done}/{total}\n{msg}"

    keyboard = []
    for hid, name, status in habits:
        icon = "✅" if status == 1 else "⬜"
        s = get_streak(hid)
        fire = f" 🔥{s}" if s >= 2 else ""
        keyboard.append([InlineKeyboardButton(
            f"{icon} {name}{fire}", callback_data=f"toggle_{hid}_{date}")])
    return text, InlineKeyboardMarkup(keyboard)

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
    today = datetime.date.today().isoformat()
    text, markup = build_today_view(update.effective_user.id, today)
    await update.message.reply_text(text, reply_markup=markup)
=======
        await update.message.reply_text("شما هنوز هیچ عادتی تعریف نکرده‌اید. از /addhabit استفاده کنید.")
        return

    keyboard = []
    for habit_id, name, status in habits:
        status_icon = "✅" if status == 1 else "❌"
        keyboard.append([InlineKeyboardButton(f"{status_icon} {name}", callback_data=f"toggle_{habit_id}_{today}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("وضعیت عادت‌های امروز شما:", reply_markup=reply_markup)
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa

# ==================== مدیریت کلیک روی دکمه‌ها ====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
<<<<<<< HEAD

=======
    
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa
    data = query.data
    if data.startswith("toggle_"):
        _, habit_id, date = data.split("_")
        habit_id = int(habit_id)
<<<<<<< HEAD

        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute("SELECT status FROM logs WHERE habit_id = ? AND date = ?",
                  (habit_id, date))
        row = c.fetchone()

        # تغییر وضعیت (اگر نبود ثبت کن، اگر بود برعکسش کن)
        if row is None:
            c.execute("INSERT INTO logs (habit_id, date, status) VALUES (?, ?, 1)",
                      (habit_id, date))
        else:
            new_status = 0 if row[0] == 1 else 1
            c.execute("UPDATE logs SET status = ? WHERE habit_id = ? AND date = ?",
                      (new_status, habit_id, date))
        conn.commit()
        conn.close()

        # به‌روزرسانی پیام (متن + نوار پیشرفت + دکمه‌ها)
        text, markup = build_today_view(query.from_user.id, date)
        await query.edit_message_text(text, reply_markup=markup)

# ==================== یادآور روزانه ====================
async def daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('habits.db')
    users = [r[0] for r in conn.execute("SELECT user_id FROM users")]
    conn.close()

    today = datetime.date.today().isoformat()
    for uid in users:
        text, markup = build_today_view(uid, today)
        if markup:  # فقط اگر کاربر عادت دارد
            await context.bot.send_message(
                uid, "⏰ یادآوری شبانه!\n\n" + text, reply_markup=markup)
=======
        
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
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa

# ==================== اجرای اصلی برنامه ====================
def main():
    if not TOKEN:
        print("خطا: توکن ربات پیدا نشد! فایل .env را بررسی کنید.")
        return

<<<<<<< HEAD
    builder = (Application.builder().token(TOKEN)
               .connect_timeout(30).read_timeout(30)
               .write_timeout(30).pool_timeout(30))
    if PROXY:
        builder = builder.proxy(PROXY).get_updates_proxy(PROXY)
    application = builder.build()
=======
    application = Application.builder().token(TOKEN).build()
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa

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

<<<<<<< HEAD
    # یادآور روزانه ساعت ۲۱:۰۰ به وقت تهران
    application.job_queue.run_daily(
        daily_reminder,
        time=datetime.time(21, 0, tzinfo=ZoneInfo("Asia/Tehran"))
    )

=======
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa
    print("ربات در حال اجراست...")
    application.run_polling()

if __name__ == '__main__':
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> acb04d9db666de947db8eea340c8c4d3ad3d37fa
