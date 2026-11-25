from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.keyboards.habit_keyboard import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "سلام! 👋\n"
        "به ربات مدیریت عادت خوش اومدی.\n\n"
        "اینجا می‌تونی عادت‌های روزانه‌ات رو مدیریت کنی "
        "و پیشرفتت رو دنبال کنی. 💪",
        reply_markup=main_menu_keyboard()
    )
