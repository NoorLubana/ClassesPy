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


def main():
    calendar = create_weekly_calendar()
    filename = "appointments1.csv"  # Default filename
    print("Starting the Appointment Manager System")
    print("Weekly calendar created")
    load_choice = input("Would you like to load previously scheduled appointments from a file (Y/N)? ").lower()
    if load_choice == 'y':
        filename = input("Enter the filename for scheduled appointments (e.g., appointments.csv): ")
        load_scheduled_appointments(filename, calendar)

    while True:
        choice = print_menu()
        if choice == '1':
            print("\n** Schedule an appointment **")
            day = input("What day: ").capitalize()
            start_hour_str = input("Enter start hour (24 hour clock): ")

            if start_hour_str.isdigit() and 0 <= int(start_hour_str) <= 23:
                start_hour = int(start_hour_str)
                appointment = find_appointment_by_time(calendar, day, start_hour)
                
                if is_slot_booked(calendar, day, start_hour):
                    print("Sorry that time slot is booked already!")
                elif appointment:
                    client_name = input("Client Name: ").capitalize()
                    client_phone = input("Client Phone: ")
                    print("Appointment types\n1: Mens Cut $50, 2: Ladies Cut $80, 3: Mens Colouring $50, 4: Ladies Colouring $120")

                    appt_type_str = input("Type of Appointment: ")
                    if appt_type_str in ['1', '2', '3', '4']:
                        appt_type = int(appt_type_str)
                        appointment.schedule(client_name, client_phone, appt_type)
                        print(f"OK, {client_name}'s appointment is scheduled!")
                    else:
                        print("Sorry that is not a valid appointment type!")
                        # Simply don't use 'continue', it will go back to the main menu
                else:
                    print("Sorry that time slot is not in the weekly calendar!")
        elif choice == '2':
            print("\n** Find appointment by name **")
            client_name = input("Enter Client Name: ").capitalize()
            found_appointments = False
            for appointment in calendar:
                if client_name in appointment.get_client_name().capitalize():
                    print(f"{'Client Name'.ljust(20)} {'Phone'.ljust(15)} {'Day'.ljust(10)} {'Start'.ljust(10)} {'End'.ljust(10)} {'Type'}")
                    print("-" * 80)
                    print(appointment)
                    found_appointments = True
            if not found_appointments:
                print("Appointment for"+ client_name)
                print(f"{'Client Name'.ljust(20)} {'Phone'.ljust(15)} {'Day'.ljust(10)} {'Start'.ljust(10)} {'End'.ljust(10)} {'Type'}")
                print("-" * 80)
                print("No appointment found.")


        elif choice == '3':
            print("\n** Print calendar for a specific day **")
            day = input("Enter day of week: ")
            print(f"{'Client Name'.ljust(20)} {'Phone'.ljust(15)} {'Day'.ljust(10)} {'Start'.ljust(10)} {'End'.ljust(10)} {'Type'}")
            print("-" * 80)
            show_appointments_by_day(calendar, day)

        elif choice == '4':
            print("\n** Cancel an appointment **")
            day = input("What day: ").capitalize()
            start_hour = int(input("Enter start hour (24 hour clock): "))
            appointment = find_appointment_by_time(calendar, day, start_hour)

            if appointment and appointment.get_client_name():  # Check if the appointment is actually booked
                client_name = appointment.get_client_name()  # Save the client's name before cancelling
                appointment.cancel()
                print(f"Appointment: {day} {start_hour:02d}:00 - {start_hour + 1:02d}:00 for {client_name} has been cancelled!")
            elif appointment:  # Appointment slot exists but no client name is associated, meaning it's not booked
                print(f"That time slot isn't booked and doesn't need to be cancelled")
            else:  # No appointment slot found for the given day and time
                print("Sorry, that time slot is not in the weekly calendar!")


        elif choice == '9':
            print("\n** Exit the system **")
            save_choice = input("Woould you like to save all scheduled appointment to a file (Y/N) ").lower()
            if save_choice in 'y':  # Check if the user wants to save
                filename = input("Enter appointment filename: ")
                save_scheduled_appointments(filename, calendar)  # Save the appointments to the file
            print("Exiting the system. Thank you!")
            break


        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
