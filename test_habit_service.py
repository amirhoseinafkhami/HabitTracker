
from services.habit_service import (
    add_habit,
    get_habits,
    remove_habit
)

user_id = 123456

# 1. Test adding a habit
print("Adding habit:")
result = add_habit(user_id, "Reading")
print(result)

# 2. Test adding an empty habit
print("\nTesting empty habit:")
result = add_habit(user_id, "   ")
print(result)

# 3. Test adding a long habit
print("\nTesting long habit:")
result = add_habit(user_id, "A" * 101)
print(result)

# 4. Test getting habits
print("\nGetting habits:")
habits = get_habits(user_id)

for habit in habits:
    print(dict(habit))

# 5. Test deleting a habit
if habits:
    habit_id = habits[0]["habit_id"]

    print("\nDeleting habit:")
    print(remove_habit(user_id, habit_id))

# 6. Test deleting a nonexistent habit
print("\nDeleting nonexistent habit:")
print(remove_habit(user_id, 999999))
