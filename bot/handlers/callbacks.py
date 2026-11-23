from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.habit_service import get_habits

router = Router()


@router.callback_query(F.data == "my_habits")
async def my_habits_handler(callback: CallbackQuery):

    user_id = callback.from_user.id

    habits = get_habits(user_id)

    if not habits:
        await callback.message.answer(
            "📭 هنوز هیچ عادتی ثبت نکردی!"
        )
    else:
        text = "📋 لیست عادت‌های شما:\n\n"

        for index, habit in enumerate(habits, start=1):
            text += f"{index}. {habit['name']}\n"

        await callback.message.answer(text)

    await callback.answer()