from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from bot.handlers.habit_states import HabitStates
from services.habit_service import add_habit

router = Router()



@router.callback_query(F.data == "add_habit")
async def add_habit_start(
        callback: CallbackQuery,
        state: FSMContext,
):
    await state.set_state(HabitStates.waiting_for_habit_name)

    await callback.message.answer(
        "✍️ اسم عادتی که می‌خوای ثبت کنی رو وارد کن:"
    )

    await callback.answer()

@router.message(HabitStates.waiting_for_habit_name, F.text)
async def receive_habit_name(
        message: Message,
        state: FSMContext,
):
    user_id = message.from_user.id
    habit_name = message.text

    success, result = add_habit(user_id, habit_name)

    if not success:
        await message.answer(
            f"⚠️ {result}\nلطفاً دوباره نام عادت رو وارد کن:"
        )
        return
    await state.clear()

    await message.answer(
        f"✅ عادت «{habit_name.strip()}» با موفقیت ثبت شد!\n\n"
        "حالا می‌تونی از منوی اصلی عادت‌هات رو مدیریت کنی."
    )