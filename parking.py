# ===== CAR PARKING MANAGEMENT SYSTEM - BACKEND =====

total_slots = 5
DATA_FILE = "parking_data.txt"


def load_parking_data():
    try:
        with open(DATA_FILE, "r") as file:
            slots = [int(line.strip()) for line in file if line.strip()]
        if len(slots) == total_slots and all(slot in (0, 1) for slot in slots):
            return slots
    except FileNotFoundError:
        pass
    except (ValueError, OSError):
        pass
    return [0, 0, 0, 0, 0]


def save_parking_data():
    try:
        with open(DATA_FILE, "w") as file:
            for slot in parking_slots:
                file.write(str(slot) + "\n")
    except OSError:
        pass


parking_slots = load_parking_data()


def park_car(slot_number):
    if 1 <= slot_number <= total_slots:
        if parking_slots[slot_number - 1] == 0:
            parking_slots[slot_number - 1] = 1
            save_parking_data()
            return "success"
        else:
            return "occupied"
    else:
        return "invalid"


def remove_car(slot_number):
    if 1 <= slot_number <= total_slots:
        if parking_slots[slot_number - 1] == 1:
            parking_slots[slot_number - 1] = 0
            save_parking_data()
            return "success"
        else:
            return "empty"
    else:
        return "invalid"


def view_status():
    return parking_slots[:]


def count_available():
    return parking_slots.count(0)


def calculate_fee(hours):
    if hours > 0:
        return hours * 100
    else:
        return None


if __name__ == "__main__":
    print("===== CAR PARKING MANAGEMENT SYSTEM =====")
    print("Parking record loaded.")

    while True:
        print("\n----- MAIN MENU -----")
        print("1. Park a Car")
        print("2. Remove a Car")
        print("3. View Parking Status")
        print("4. View Available Slots")
        print("5. Calculate Parking Fee")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            try:
                slot = int(input("Enter parking slot number (1-5): "))
                result = park_car(slot)
                if result == "success":
                    print("Car successfully parked!")
                elif result == "occupied":
                    print("Sorry! This slot is already occupied.")
                else:
                    print("Invalid slot number!")
            except ValueError:
                print("Please enter a valid number!")

        elif choice == "2":
            try:
                slot = int(input("Enter slot number to remove car (1-5): "))
                result = remove_car(slot)
                if result == "success":
                    print("Car successfully removed!")
                elif result == "empty":
                    print("This slot is already empty.")
                else:
                    print("Invalid slot number!")
            except ValueError:
                print("Please enter a valid number!")

        elif choice == "3":
            print("----- Parking Status -----")
            for i, s in enumerate(view_status()):
                status = "Available" if s == 0 else "Occupied"
                print(f"Slot {i+1} is {status}")

        elif choice == "4":
            print("Available Slots:", count_available())
            for i, s in enumerate(view_status()):
                if s == 0:
                    print(f"Slot {i+1} is Available")

        elif choice == "5":
            try:
                hours = int(input("Enter parking hours: "))
                fee = calculate_fee(hours)
                if fee:
                    print(f"Total Parking Fee: Rs. {fee}")
                else:
                    print("Invalid hours!")
            except ValueError:
                print("Please enter a valid number!")

        elif choice == "6":
            print("Thank you for using Car Parking Management System!")
            print("Program ended.")
            break

        else:
            print("Invalid choice! Please select 1-6.")