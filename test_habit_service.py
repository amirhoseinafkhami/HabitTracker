from services.habit_service import (
    add_habit,
    get_daily_habits_service,
    set_habit_status_service,
    get_habits
)

user_id = 123456

# 1. Create a test habit
print("Creating test habit:")
print(add_habit(user_id, "Test Habit"))

# 2. Get user's habits
habits = get_habits(user_id)

print("\nUser habits:")

for habit in habits:
    print(dict(habit))

# 3. Select the first habit
if habits:
    habit_id = habits[0]["habit_id"]

    # 4. Mark habit as completed
    print("\nMarking habit as completed:")
    print(set_habit_status_service(user_id, habit_id, 1))

    # 5. Get daily habits
    print("\nDaily habits:")

    daily_habits = get_daily_habits_service(user_id)

    for habit in daily_habits:
        print(dict(habit))

    # 6. Mark habit as incomplete
    print("\nMarking habit as incomplete:")
    print(set_habit_status_service(user_id, habit_id, 0))

else:
    print("No habits found!")