from datetime import datetime, timedelta

def get_lesson_dates(weekday):
    # weekday: 0 - понедельник, 1 - вторник, 2 - среда, и т.д.
    start_date = datetime.now()
    end_date = start_date + timedelta(days=38)
    dates = []
    
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == weekday:  # проверяем нужный день недели
            dates.append(current_date.date())
        current_date += timedelta(days=1)
    
    return dates

# Пример для суббот (5):
saturday_dates = get_lesson_dates(5)
print("Субботы:")
for date in saturday_dates:
    print(date.strftime('%d.%m.%Y'))