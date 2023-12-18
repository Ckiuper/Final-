import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime

class EventMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EventMaster")
        self.root.geometry("600x400")

        # Welcome message
        ttk.Label(root, text="Welcome to EventMaster", font=("Helvetica", 16)).pack(pady=10)

        # Display today's date and summary of upcoming events
        self.display_date_summary()

        # Buttons for navigation with images
        calendar_img = tk.PhotoImage(file="calendar.png")
        add_event_img = tk.PhotoImage(file="addevent.png")
        exit_img = tk.PhotoImage(file="exit.png")

        ttk.Button(root, text="View Calendar", command=self.show_calendar, image=calendar_img, compound=tk.LEFT).pack(pady=10)
        ttk.Button(root, text="Add New Event", command=self.show_event_creation, image=add_event_img, compound=tk.LEFT).pack(pady=10)
        ttk.Button(root, text="Exit", command=root.destroy, image=exit_img, compound=tk.LEFT).pack(pady=10)

        # List to store user-added event dates
        self.user_added_dates = []

    def display_date_summary(self):
        # You can implement logic here to display today's date and summary of upcoming events
        # For demonstration, let's print a message
        print("Displaying date summary...")

    def show_calendar(self):
        # Create a new top-level window for the calendar view
        self.cal_window = tk.Toplevel(self.root)
        self.cal_window.title("Calendar View")
        self.cal_window.geometry("600x500")

        # Create a Calendar widget
        self.cal = Calendar(self.cal_window, selectmode="day")
        self.cal.pack(pady=10)

        # Highlight dates with scheduled events (user-added dates)
        for date_str in self.user_added_dates:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            self.cal.calevent_create(date_obj, "Event", "event")

        # Buttons for month navigation with images
        prev_month_img = tk.PhotoImage(file="prevmonth.png")
        next_month_img = tk.PhotoImage(file="nextmonth.png")

        ttk.Button(self.cal_window, command=self.cal.prev_month, image=prev_month_img, compound=tk.LEFT).pack(side=tk.LEFT)
        ttk.Button(self.cal_window, command=self.cal.next_month, image=next_month_img, compound=tk.LEFT).pack(side=tk.RIGHT)

        # Frame to display event preview
        self.event_preview_frame = ttk.Frame(self.cal_window)
        self.event_preview_frame.pack(pady=10)

        # Define self.cal_window here
        self.cal_window.protocol("WM_DELETE_WINDOW", self.destroy_cal_window)

    def update_event_preview(self, event=None):
        # Clear existing widgets in the event preview frame
        for widget in self.event_preview_frame.winfo_children():
            widget.destroy()

        # Get the selected date from the calendar
        selected_date = self.cal.selection_get()

        if selected_date:
            # Format the selected date as a string
            selected_date_str = selected_date.strftime("%Y-%m-%d")

            # Check if there is an event on the selected date
            if selected_date_str in self.user_added_dates:
                # Display event details in the event preview frame
                ttk.Label(self.event_preview_frame, text=f"Event Details for {selected_date_str}:", font=("Helvetica", 12)).pack()

                # Replace placeholders with actual event details
                event_details = self.get_event_details(selected_date_str)

                ttk.Label(self.event_preview_frame, text=f"Event Title: {event_details['title']}", font=("Helvetica", 10)).pack()
                ttk.Label(self.event_preview_frame, text=f"Event Time: {event_details['time']}", font=("Helvetica", 10)).pack()
                ttk.Label(self.event_preview_frame, text=f"Location: {event_details['location']}", font=("Helvetica", 10)).pack()

    def get_event_details(self, date_str):
        # Replace this with your logic to retrieve event details for a given date (customize this)
        # For demonstration, return sample event details
        event_details = {
            'title': 'Sample Event',
            'time': '3:00 PM',
            'location': 'Sample Location',
        }
        return event_details

    def show_event_creation(self):
        # Create a new top-level window for event creation
        self.event_window = tk.Toplevel(self.root)
        self.event_window.title("Event Creation")
        self.event_window.geometry("600x450")

        # Add labels, images, and buttons for event details
        ttk.Label(self.event_window, text="Event Title:", font=("Helvetica", 12)).pack(pady=5)
        title_entry = ttk.Entry(self.event_window, font=("Helvetica", 12))
        title_entry.pack(pady=5)

        ttk.Label(self.event_window, text="Event Date (mm/dd/yyyy):", font=("Helvetica", 12)).pack(pady=5)
        date_entry = DateEntry(self.event_window, font=("Helvetica", 12), date_pattern="mm/dd/yyyy")
        date_entry.pack(pady=5)

        ttk.Label(self.event_window, text="Notes:", font=("Helvetica", 12)).pack(pady=5)
        notes_text = tk.Text(self.event_window, wrap=tk.WORD, width=40, height=5)
        notes_text.pack(pady=5)

        # Option to set reminders and notifications (customize this)
        reminder_var = tk.IntVar()
        ttk.Checkbutton(self.event_window, text="Set Reminder", variable=reminder_var).pack(pady=5)

        # Save and cancel buttons for event creation with images
        save_img = tk.PhotoImage(file="save.png")
        cancel_img = tk.PhotoImage(file="cancel.png")

        save_button = ttk.Button(self.event_window, command=lambda: self.save_event(title_entry.get(), date_entry.get(), "", notes_text.get("1.0", tk.END), reminder_var.get()),
                                 image=save_img, compound=tk.NONE)
        save_button.image = save_img  # Retain reference to the image
        save_button.pack(side=tk.LEFT, padx=10)

        cancel_button = ttk.Button(self.event_window, command=self.event_window.destroy,
                                   image=cancel_img, compound=tk.NONE)
        cancel_button.image = cancel_img  # Retain reference to the image
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def save_event(self, title, date, address, notes, reminder):
        # Input validation
        if not title or not date:
            # Display an error message
            error_message = "Error: Please fill in all required fields."
            self.show_error_message(error_message)
            return

        try:
            date_obj = datetime.strptime(date, "%m/%d/%Y").date()
        except ValueError:
            # Display an error message for invalid date format
            error_message = "Invalid date format. Please enter in MM/DD/YYYY format."
            self.show_error_message(error_message)
            return

        # Print event details (customize as needed)
        print("Event Title:", title)
        print("Event Date:", date_obj.strftime("%Y-%m-%d"))  # Format the date as needed
        print("Notes:", notes)
        print("Set Reminder:", reminder)

        # Add reminders and notifications logic here (customize as needed)
        if reminder:
            print("Reminder set!")

        # Update the calendar with the new event
        self.user_added_dates.append(date_obj.strftime("%Y-%m-%d"))
        self.update_calendar(date, title)

        # Destroy the event creation window after saving the event
        self.event_window.destroy()

    def show_error_message(self, message):
        # Create a top-level window for displaying error messages
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_window.geometry("300x100")

        # Display the error message
        ttk.Label(error_window, text=message, font=("Helvetica", 12), foreground="red").pack(pady=20)

        # Add a close button to close the error window
        close_button = ttk.Button(error_window, text="Close", command=error_window.destroy)
        close_button.pack(pady=10)

    def update_calendar(self, date_str, event_title):
        # Convert date string to datetime object
        date_obj = datetime.strptime(date_str, "%m/%d/%Y").date()

        # Check if the calendar window is open
        if hasattr(self, 'cal_window') and self.cal_window.winfo_exists():
            # Add the event to the calendar widget
            self.cal.calevent_create(date_obj, event_title, "event")
            self.cal.tag_config("event", background="lightblue")

    def destroy_cal_window(self):
        # Destroy the calendar window and reset self.cal_window to None
        if hasattr(self, 'cal_window') and self.cal_window.winfo_exists():
            self.cal_window.destroy()
            self.cal_window = None

if __name__ == "__main__":
    root = tk.Tk()
    app = EventMasterApp(root)
    root.mainloop()
