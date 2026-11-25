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

def habits_list_keyboard(habits):
    builder = InlineKeyboardBuilder()
    for habit in habits:
        builder.button(
            text=f"حذف عادت ❌{habit['name']}",
            callback_data=f"delete_habit: {habit['habit_id']}"
        )

    builder.adjust(1)

    return builder.as_markup()


def daily_habits_keyboard(habits):
    builder = InlineKeyboardBuilder()

    for habit in habits:
        habit_id = habit["habit_id"]

        builder.button(
            text="✅ انجام شد",
            callback_data=f"habit_status:{habit_id}:1"
        )

        builder.button(
            text="❌ انجام نشد",
            callback_data=f"habit_status:{habit_id}:0"
        )

        builder.adjust(2)

    return builder.as_markup()

