
from services.habit_service import get_daily_habits_service

user_id = 123456

habits = get_daily_habits_service(user_id)

print("Daily habits returned from service:")

for habit in habits:
    print(dict(habit))

print("Total habits:", len(habits))
