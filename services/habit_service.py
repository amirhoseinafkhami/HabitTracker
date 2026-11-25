from datetime import date
from database.repositories.habit_repository import (
    create_habit,
    get_user_habits,
    delete_habit,
    mark_habit,
    get_daily_habits
)

def add_habit(user_id: int, name: str):
    name = name.strip()

    if not name:
        return False, "نام عادت نمیتواند خالی باشد"

    if len(name) > 100:
        return False, "نام عادت نمیتواند بیشتر از 100 کاراکتر باشد"

    habit_id = create_habit(user_id, name)

    return True, habit_id

def get_habits(user_id: int):
    return get_user_habits(user_id)

def remove_habit(user_id: int, habit_id: int):
    deleted = delete_habit(habit_id, user_id)

    if deleted == 0:
        return False, "عادت موردنظر پیدا نشد."

    return True, "عادت با موفقیت حذف شد."

def get_daily_habits_service(user_id: int):
    today = date.today().isoformat()

    return get_daily_habits(user_id, today)

def set_habit_status_service(user_id: int, habit_id: int, status: int):
    if status not in (0, 1):
        return False, "وضعیت نامعتبر است..."

    today = date.today().isoformat()

    result = mark_habit(user_id, habit_id, today, status)

    if result == 0:
        return False, "عادت موردنظر پیدا نشد."

    if status == 1:
        return True, "عادت با موفقیت انجام شد! 🎉"

    return True, "وضعیت عادت به انجام‌نشده تغییر کرد."
