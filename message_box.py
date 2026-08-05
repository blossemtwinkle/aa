from datetime import datetime
import threading
import time
import tkinter as tk
from tkinter import messagebox
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS

# Hide Tkinter root window
root = tk.Tk()
root.withdraw()

app = Flask(__name__)
CORS(app)

# Global timetable data storage
timetable_db = {
    "Mon": [],
    "Tue": [],
    "Wed": [],
    "Thu": [],
    "Fri": [],
}


def trigger_desktop_notification(title, message):
    """Displays desktop notification box without blocking Flask."""
    messagebox.showinfo(title, message)


def reminder_loop():
    """Background loop checking for scheduled class times every 30 seconds."""
    already_notified = set()

    while True:
        now = datetime.now()
        current_day = now.strftime("%a")  # e.g., 'Mon'
        current_time_str = now.strftime("%H:%M")  # e.g., '14:30'

        day_items = timetable_db.get(current_day, [])

        for item in day_items:
            item_time = item.get("time", "").strip()
            subject = item.get("subject", "").strip()

            notif_id = f"{current_day}-{item_time}-{subject}"

            if item_time == current_time_str and notif_id not in already_notified:
                already_notified.add(notif_id)

                title = "Class / Meeting Reminder!"
                msg = f"Time: {current_time_str}\nNext: {subject}\nDetails: {item.get('dueDate', 'N/A')}"

                # Run popup in separate thread so it doesn't freeze the backend
                threading.Thread(
                    target=trigger_desktop_notification, args=(title, msg)
                ).start()

        time.sleep(30)


# Start the background reminder thread
threading.Thread(target=reminder_loop, daemon=True).start()


@app.route("/")
def index():
    """Serves schedule.html directly."""
    try:
        with open("schedule.html", "r", encoding="utf-8") as f:
            return render_template_string(f.read())
    except FileNotFoundError:
        return "Error: schedule.html not found in the same folder!", 404


@app.route("/api/get-schedule", methods=["GET"])
def get_schedule():
    """Endpoint for JavaScript to fetch timetable on page load."""
    return jsonify({"value": timetable_db})


@app.route("/api/save-schedule", methods=["POST"])
def save_schedule():
    """Endpoint for JavaScript to save timetable updates."""
    global timetable_db
    input_data = request.json.get("value")

    if input_data:
        timetable_db = input_data

    # Show Tkinter confirmation popup in a separate thread
    threading.Thread(
        target=trigger_desktop_notification,
        args=(
            "Good Plan Better Life",
            "Schedule saved successfully! Reminders are active.",
        ),
    ).start()

    return jsonify({"status": "success", "message": "Saved!"})


if __name__ == "__main__":
    # Pop up initial startup message in background so Flask starts immediately!
    threading.Thread(
        target=trigger_desktop_notification,
        args=("Good Plan Better Life", "Reminder system is working!"),
    ).start()

    # Start Flask Server
    app.run(port=5000, debug=False)