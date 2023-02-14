import datetime

#A python module that stores all the global variables for this application.
current_time = datetime.datetime.today().replace(hour=8, minute=0, second=0)
work_start_time = datetime.datetime.today().replace(hour=8, minute=0, second=0)
start_time = datetime.datetime.today().replace(hour=8, minute=0, second=0)
end_time = datetime.datetime.today().replace(hour=8, minute=0, second=0)
total_miles = 0.0

#A function to update the current time with the time that a user inputs.
#It uses exception handling to make validating the user's input easier.
def set_time(time:datetime, time_type: str) -> datetime:
    user_time_string = input(f"Set the {time_type} time using the format HH:MM am/pm: ")
    user_time = datetime.datetime.strptime(user_time_string, "%H:%M %p")
    return time.replace(hour=user_time.hour, minute=user_time.minute,
                                       second=0, microsecond= 0)