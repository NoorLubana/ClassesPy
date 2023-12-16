# appt_manager.py
from appointment import Appointment

def create_weekly_calendar():
    calendar = []
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    for day in days_of_week:
        for hour in range(9, 17):
            appointment = Appointment(day, hour)
            calendar.append(appointment)

    return calendar

def load_scheduled_appointments(filename, calendar):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                values = line.strip().split(',')
                day_of_week = values[3]
                start_time_hour = int(values[4])
                appointment = find_appointment_by_time(calendar, day_of_week, start_time_hour)
                if appointment:
                    appointment.schedule(values[0], values[1], int(values[2]))

def is_slot_booked(calendar, day, start_hour):
    for appointment in calendar:
        if appointment.get_day_of_week() == day and appointment.get_start_time_hour() == start_hour and appointment.get_client_name() != "":
            return True
    return False

def print_menu():
    print("\n")
    print("Jojo's Hair Salon Appointment Manager")
    print("=" * 37)
    print("1) Schedule an appointment")
    print("2) Find appointment by name")
    print("3) Print calendar for a specific day")
    print("4) Cancel an appointment")
    print("9) Exit the system")

    return input("Enter your selection:")

def find_appointment_by_time(calendar, day, start_hour):
    for appointment in calendar:
        if appointment.get_day_of_week() == day and appointment.get_start_time_hour() == start_hour:
            return appointment
    return None

def show_appointments_by_name(calendar, name):
    for appointment in calendar:
        if name.lower() in appointment.get_client_name().lower():
            print(appointment)



def show_appointments_by_day(calendar, day):
    print("\n** Print calendar for a specific day **")
    print(f"Appointments for {day.capitalize()}")
    print(f"{'Client Name'.ljust(20)} {'Phone'.ljust(15)} {'Day'.ljust(10)} {'Start'.ljust(10)} {'End'.ljust(10)} {'Type'}")
    print("-" * 80)

    for appointment in calendar:
        if appointment.get_day_of_week().lower() == day.lower():
            client_name = appointment.get_client_name() if appointment.get_client_name() else " "
            client_phone = appointment.get_client_phone() if appointment.get_client_phone() else " "
            start_time = f"{appointment.get_start_time_hour():02d}:00"
            end_time = f"{appointment.get_start_time_hour() + 1:02d}:00"  # Assuming 1 hour appointments
            appt_type = appointment.get_appt_type_desc() if appointment.get_client_name() else "Available"
            
            print(f"{client_name.ljust(20)} {client_phone.ljust(15)} {day.capitalize().ljust(10)} {start_time.ljust(10)} {end_time.ljust(10)} {appt_type}")



def save_scheduled_appointments(filename, calendar):
    saved_count = 0  # Initialize a counter for saved appointments
    with open(filename, 'w') as file:
        for appointment in calendar:
            if appointment.get_appt_type() != 0:
                file.write(appointment.format_record() + '\n')
                saved_count += 1  # Increment the counter for each saved appointment
    print(f"{saved_count} scheduled appointments have been successfully saved to {filename}.")
