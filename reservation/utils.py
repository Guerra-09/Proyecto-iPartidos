from datetime import time, timedelta, datetime, date


# def get_all_possible_times_for_a_day(tenant):
       

#     start_time = tenant.clubApertureTime  # 14:00
#     end_time = tenant.clubClosureTime  # 00:00
#     interval = timedelta(hours=1)

#     print(f"Start time: {start_time}, End time: {end_time}")

       
#     if end_time < start_time:
#         end_time = datetime.combine(date.today() + timedelta(days=1), end_time).time()


    
#     current_time = start_time
#     all_times = []
#     while current_time < end_time:
#         all_times.append(current_time.strftime("%H:%M"))
#         current_time = (datetime.combine(date.today(), current_time) + interval).time()
#         if current_time > time(23, 59):
#             current_time = time()

#     return all_times

def get_all_possible_times_for_a_day(tenant):
    start_time = tenant.clubApertureTime  # 10:00
    end_time = tenant.clubClosureTime  # 00:00
    interval = timedelta(hours=1)

    print(f"Start time: {start_time}, End time: {end_time}")

    current_time = start_time
    all_times = []

    while True:
        all_times.append(current_time.strftime("%H:%M"))
        current_time = (datetime.combine(date.today(), current_time) + interval).time()
        if current_time == start_time or (end_time == time() and current_time == time(1, 0)):
            break

    return all_times

def get_all_possible_times_for_a_day(tenant):
    start_time = tenant.clubApertureTime  # 10:00
    end_time = tenant.clubClosureTime  # 00:00
    interval = timedelta(hours=1)

    print(f"Start time: {start_time}, End time: {end_time}")

    current_time = start_time
    all_times = []

    while True:
        all_times.append(current_time.strftime("%H:%M"))
        current_time = (datetime.combine(date.today(), current_time) + interval).time()
        if current_time == start_time or (end_time == time() and current_time == time(0, 0)):
            break

    return all_times