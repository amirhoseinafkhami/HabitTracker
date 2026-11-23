
from database.repositories.habit_repository import (
    create_habit,
    get_user_habits,
    delete_habit
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
