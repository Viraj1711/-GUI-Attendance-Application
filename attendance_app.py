import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Create a connection to the SQLite database
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Create the Attendance table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    status TEXT NOT NULL)''')
conn.commit()

# Function to mark attendance
def mark_attendance():
    name = entry_name.get()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return
    
    status = "Present"
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Insert the attendance record into the database
    cursor.execute("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)", (name, date, status))
    conn.commit()
    
    messagebox.showinfo("Attendance", f"Attendance marked for {name} at {date}")
    entry_name.delete(0, tk.END)

# Function to view attendance records
def view_attendance():
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    
    if not records:
        messagebox.showinfo("No Records", "No attendance records found.")
        return
    
    # Create a new window to display the records
    records_window = tk.Toplevel(root)
    records_window.title("Attendance Records")
    
    # Displaying the records
    for i, record in enumerate(records):
        tk.Label(records_window, text=f"{record[1]} | {record[2]} | {record[3]}").grid(row=i, column=0, padx=10, pady=5)
    
# Create the main window
root = tk.Tk()
root.title("Attendance Application")
root.geometry("400x300")

# Add widgets to the window
tk.Label(root, text="Enter Name:").pack(pady=10)
entry_name = tk.Entry(root)
entry_name.pack(pady=10)

btn_mark = tk.Button(root, text="Mark Attendance", command=mark_attendance)
btn_mark.pack(pady=10)

btn_view = tk.Button(root, text="View Attendance Records", command=view_attendance)
btn_view.pack(pady=10)

# Start the GUI event loop
root.mainloop()

# Close the database connection when the program is closed
conn.close()
