from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="➕ افزودن عادت جدید",
        callback_data= "add_habit",
    )

    builder.button(
        text= "📋 عادت‌های من",
        callback_data= "my_habits"
    )

    builder.adjust(1)

    return builder.as_markup()