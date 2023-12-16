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