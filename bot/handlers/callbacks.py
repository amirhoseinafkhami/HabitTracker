from datetime import date
from aiogram import Router, F
from aiogram.types import CallbackQuery


from services.habit_service import get_habits
from services.habit_service import remove_habit
from bot.keyboards.habit_keyboard import habits_list_keyboard, daily_habits_keyboard
from services.habit_service import set_habit_status_service, get_daily_habits_service


router = Router()


@router.callback_query(F.data.startswith("delete_habit"))
async def delete_habit_handler(callback: CallbackQuery):

    user_id = callback.from_user.id
    habit_id = int(callback.data.split(":")[1])

    success, message = remove_habit(user_id, habit_id)

    await callback.answer(
        message,
        show_alert=True,
    )

    if success:
        await callback.message.edit_reply_markup(
            reply_markup = None
        )


@router.callback_query(F.data.startswith("habit_status:"))
async def habit_status_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    # دریافت شناسه عادت و وضعیت انتخاب‌شده
    _, habit_id, status = callback.data.split(":")

    habit_id = int(habit_id)
    status = int(status)

    # ثبت وضعیت عادت
    success, message = set_habit_status_service(
        user_id,
        habit_id,
        status
    )

    if not success:
        await callback.answer(
            message,
            show_alert=True,
        )
        return

    habits = get_daily_habits_service(user_id)

    text = "📅 عادت‌های امروز:\n\n"
    print("USER ID:", user_id)
    print("HABITS:", [dict(habit) for habit in habits])

    for index, habit in enumerate(habits, start=1):
        habit_status = (
            "✅ انجام شده"
            if habit["status"] == 1
            else "⏳ انجام نشده"
        )

        text += (
            f"{index}. {habit['name']}\n"
            f"وضعیت: {habit_status}\n\n"
        )

        # به‌روزرسانی پیام قبلی
    await callback.message.edit_text(
        text,
        reply_markup=daily_habits_keyboard(habits)
    )

    await callback.answer(message)


@router.callback_query(F.data == "my_habits")
async def my_habits_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    habits = get_daily_habits_service(user_id)

    if not habits:
        await callback.message.answer(
            "📭 هنوز هیچ عادتی ثبت نکردی!"
        )
    else:
        text = f"📅 عادت‌های امروز ({date.today()}):\n\n"

        for index, habit in enumerate(habits, start=1):
            status = "✅ انجام شده" if habit["status"] == 1 else "⏳ انجام نشده"

            text += (
                f"{index}. {habit['name']}\n"
                f"وضعیت: {status}\n\n"
            )
        print("GENERATED TEXT:", text)
        await callback.message.answer(
            text,
            reply_markup=daily_habits_keyboard(habits)
        )

    await callback.answer()
