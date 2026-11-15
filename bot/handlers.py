from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

# start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer( "سلام! 👋\n"
        "به ربات مدیریت عادت‌های روزانه خوش اومدی.\n\n"
        "اینجا قراره بهت کمک کنیم عادت‌های خوبی بسازی! 🚀")

# help
@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("راهنمای ربات 📚\n\n"
        "/start - شروع کار با ربات\n"
        "/help - راهنمای دستورات")