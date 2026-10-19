# ===== CAR PARKING MANAGEMENT SYSTEM - GUI =====

import tkinter as tk
from tkinter import messagebox
import parking  # hamara backend

# ===== MAIN WINDOW =====
window = tk.Tk()
window.title("Car Parking Management System")
window.geometry("500x620")
window.resizable(False, False)
window.configure(bg="#1a1a2e")

# ===== HEADING =====
heading = tk.Label(
    window,
    text="🚗 Car Parking Management System",
    font=("Arial", 15, "bold"),
    bg="#1a1a2e",
    fg="#e0e0e0"
)
heading.pack(pady=15)

# ===== AVAILABLE SLOTS LABEL =====
available_label = tk.Label(
    window,
    text="",
    font=("Arial", 11),
    bg="#1a1a2e",
    fg="#a0d4a0"
)
available_label.pack()

# ===== SLOT BUTTONS FRAME =====
slots_frame = tk.Frame(window, bg="#1a1a2e")
slots_frame.pack(pady=15)

slot_buttons = []

for i in range(5):
    btn = tk.Button(
        slots_frame,
        text=f"Slot {i+1}\nAvailable",
        width=8,
        height=3,
        font=("Arial", 10, "bold"),
        bg="#2d6a2d",
        fg="white",
        relief="raised",
        bd=3
    )
    btn.grid(row=0, column=i, padx=8)
    slot_buttons.append(btn)

# ===== STATUS UPDATE FUNCTION =====
def update_display():
    slots = parking.view_status()
    available = parking.count_available()

    available_label.config(
        text=f"✅ Available Slots: {available} / 5"
    )

    for i in range(5):
        if slots[i] == 0:
            slot_buttons[i].config(
                text=f"Slot {i+1}\nAvailable",
                bg="#2d6a2d"
            )
        else:
            slot_buttons[i].config(
                text=f"Slot {i+1}\nOccupied",
                bg="#8b1a1a"
            )

# ===== PARK CAR FUNCTION =====
def park_car_gui():
    slot = slot_entry.get()
    try:
        slot = int(slot)
        result = parking.park_car(slot)
        if result == "success":
            messagebox.showinfo("Success", f"✅ Car parked in Slot {slot}!")
        elif result == "occupied":
            messagebox.showwarning("Occupied", f"❌ Slot {slot} is already occupied!")
        else:
            messagebox.showerror("Invalid", "⚠️ Please enter a slot number between 1 and 5!")
    except ValueError:
        messagebox.showerror("Invalid", "⚠️ Please enter a valid number!")

    slot_entry.delete(0, tk.END)
    update_display()

# ===== REMOVE CAR FUNCTION =====
def remove_car_gui():
    slot = slot_entry.get()
    try:
        slot = int(slot)
        result = parking.remove_car(slot)
        if result == "success":
            messagebox.showinfo("Success", f"✅ Car removed from Slot {slot}!")
        elif result == "empty":
            messagebox.showwarning("Empty", f"⚠️ Slot {slot} is already empty!")
        else:
            messagebox.showerror("Invalid", "⚠️ Please enter a slot number between 1 and 5!")
    except ValueError:
        messagebox.showerror("Invalid", "⚠️ Please enter a valid number!")

    slot_entry.delete(0, tk.END)
    update_display()

# ===== SLOT INPUT SECTION =====
input_frame = tk.Frame(window, bg="#1a1a2e")
input_frame.pack(pady=10)

tk.Label(
    input_frame,
    text="Enter Slot Number (1-5):",
    font=("Arial", 11),
    bg="#1a1a2e",
    fg="#e0e0e0"
).grid(row=0, column=0, columnspan=2, pady=5)

slot_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=10,
    justify="center"
)
slot_entry.grid(row=1, column=0, columnspan=2, pady=5)

# Park & Remove Buttons
tk.Button(
    input_frame,
    text="🚗 Park Car",
    font=("Arial", 11, "bold"),
    bg="#2471a3",
    fg="white",
    width=12,
    command=park_car_gui
).grid(row=2, column=0, padx=10, pady=8)

tk.Button(
    input_frame,
    text="❌ Remove Car",
    font=("Arial", 11, "bold"),
    bg="#922b21",
    fg="white",
    width=12,
    command=remove_car_gui
).grid(row=2, column=1, padx=10, pady=8)

# ===== FEE CALCULATOR SECTION =====
fee_frame = tk.LabelFrame(
    window,
    text=" 💰 Fee Calculator ",
    font=("Arial", 11, "bold"),
    bg="#1a1a2e",
    fg="#e0e0e0",
    bd=2
)
fee_frame.pack(pady=10, padx=30, fill="x")

tk.Label(
    fee_frame,
    text="Enter Hours:",
    font=("Arial", 11),
    bg="#1a1a2e",
    fg="#e0e0e0"
).grid(row=0, column=0, padx=10, pady=8)

hours_entry = tk.Entry(
    fee_frame,
    font=("Arial", 12),
    width=8,
    justify="center"
)
hours_entry.grid(row=0, column=1, padx=10, pady=8)

fee_result_label = tk.Label(
    fee_frame,
    text="Fee: Rs. 0",
    font=("Arial", 12, "bold"),
    bg="#1a1a2e",
    fg="#f7dc6f"
)
fee_result_label.grid(row=0, column=2, padx=10, pady=8)

def calculate_fee_gui():
    hours = hours_entry.get()
    try:
        hours = int(hours)
        fee = parking.calculate_fee(hours)
        if fee:
            fee_result_label.config(text=f"Fee: Rs. {fee}")
        else:
            messagebox.showerror("Invalid", "⚠️ Hours must be greater than 0!")
    except ValueError:
        messagebox.showerror("Invalid", "⚠️ Please enter a valid number!")

tk.Button(
    fee_frame,
    text="Calculate",
    font=("Arial", 10, "bold"),
    bg="#1e8449",
    fg="white",
    command=calculate_fee_gui
).grid(row=0, column=3, padx=10, pady=8)

# ===== EXIT BUTTON =====
tk.Button(
    window,
    text="🚪 Exit",
    font=("Arial", 11, "bold"),
    bg="#555555",
    fg="white",
    width=15,
    command=window.destroy
).pack(pady=20)

# ===== START =====
update_display()
window.mainloop()