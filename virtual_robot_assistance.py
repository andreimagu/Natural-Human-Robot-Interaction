import tkinter as tk
import random
import pyttsx3
import threading
from datetime import datetime
import pytz

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# List and select a friendly voice
voices = tts_engine.getProperty('voices')

# Select a voice
for voice in voices:
    if "male" in voice.name.lower(): 
        tts_engine.setProperty('voice', voice.id)
        break

# Adjust speech rate
tts_engine.setProperty('rate', 180)

# Adjust volume
tts_engine.setProperty('volume', 0.6)

# Predefined exercises, medication, and jokes database
TIME_OPTIONS = ["Morning", "Afternoon", "Evening"]

EXERCISES = {
    "Morning": ["15-minute yoga session", "Brisk 20-minute walk", "5-minute stretching routine"],
    "Afternoon": ["30-minute light cardio workout", "10-minute desk stretches", "15-minute meditation session"],
    "Evening": ["20-minute relaxing yoga", "Short evening walk", "Breathing exercises to wind down"],
}

MEDICATIONS = {
    "Morning": "Take your morning vitamins or prescribed medication.",
    "Afternoon": "Check if you need to take your afternoon pills.",
    "Evening": "Don’t forget to take your evening medication.",
}

JOKES = {
    "Morning": {
        "dark": ["Why don’t graveyards ever get overcrowded? Because people are dying to get in!",
                 "What’s the best thing about dead jokes? They never get old."],
        "light": ["Why don’t skeletons fight each other? They don’t have the guts!",
                  "What did one wall say to the other wall? I'll meet you at the corner!"],
    },
    "Afternoon": {
        "dark": ["Why do ghosts never lie? Because they’re transparent.",
                 "What’s a zombie’s favorite cereal? Rice Creepies."],
        "light": ["Why did the math book look sad? It had too many problems!",
                  "Why don’t scientists trust atoms? Because they make up everything!"],
    },
    "Evening": {
        "dark": ["What do you call a vampire who loves vegetables? A blood-thirsty vegan.",
                 "What do you call a dead comedian? A laugh-stock."],
        "light": ["Why did the bicycle fall over? It was two-tired!",
                  "How do you organize a space party? You planet!"],
    },
}

# Global variables
selected_time = None
user_name = ""
base_font_size = 8
scaled_font_size = int(base_font_size * 2)  # Increase text size by 200%


def speak(text):
    """Converts text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()
    enable_buttons()  # Re-enable buttons after speech


def disable_buttons():
    """Disables all buttons in the button frame."""
    for widget in button_frame.winfo_children():
        widget.config(state=tk.DISABLED)


def enable_buttons():
    """Re-enables all buttons in the button frame."""
    for widget in button_frame.winfo_children():
        widget.config(state=tk.NORMAL)


def handle_time_selection(time):
    """Handles the time selection and opens the next menu."""
    global selected_time
    selected_time = time

    disable_buttons()

    # Display the greeting immediately
    greeting = f"Good {time.lower()}, {user_name}! How can I assist you?"
    chat_log.config(state=tk.NORMAL)
    chat_log.delete(1.0, tk.END)
    chat_log.insert(tk.END, f"Assistant: {greeting}\n\n")
    chat_log.config(state=tk.DISABLED)

    # Start speech in a thread
    threading.Thread(target=speak, args=(greeting,)).start()
    show_main_menu()


def show_main_menu():
    """Displays the menu for exercises, medication, and jokes based on the selected time."""
    # Clear existing buttons
    for widget in button_frame.winfo_children():
        widget.destroy()

    # Add buttons for exercises, medication, jokes, and back
    tk.Button(button_frame, text="View Exercises", command=show_exercises, font=("Helvetica", scaled_font_size)).pack(
        side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="View Medication", command=show_medication, font=("Helvetica", scaled_font_size)).pack(
        side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Jokes", command=show_jokes_menu, font=("Helvetica", scaled_font_size)).pack(
        side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Back", command=show_time_selection, font=("Helvetica", scaled_font_size)).pack(
        side=tk.LEFT, padx=5)


def show_exercises():
    """Displays exercises for the selected time."""
    global selected_time
    disable_buttons()
    exercises = EXERCISES.get(selected_time, [])
    exercise_text = "\n".join([f"- {exercise}" for exercise in exercises])
    message = f"Here are some {selected_time.lower()} exercises, {user_name}:\n{exercise_text}"

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"Assistant: {message}\n\n")
    chat_log.config(state=tk.DISABLED)

    threading.Thread(target=speak, args=(message,)).start()


def show_medication():
    """Displays medication reminders for the selected time."""
    global selected_time
    disable_buttons()
    medication = MEDICATIONS.get(selected_time, f"No medication reminders for this time, {user_name}.")

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"Assistant: {medication}\n\n")
    chat_log.config(state=tk.DISABLED)

    threading.Thread(target=speak, args=(medication,)).start()


def show_jokes_menu():
    """Displays the joke options (Dark Humor, Light Humor)."""
    # Clear existing buttons
    for widget in button_frame.winfo_children():
        widget.destroy()

    # Add buttons for dark and light humor
    tk.Button(button_frame, text="Dark Humor", command=lambda: show_joke("dark"),
              font=("Helvetica", scaled_font_size)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Light Humor", command=lambda: show_joke("light"),
              font=("Helvetica", scaled_font_size)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Back", command=show_main_menu, font=("Helvetica", scaled_font_size)).pack(
        side=tk.LEFT, padx=5)


def show_joke(joke_type):
    """Displays a random joke based on the selected type."""
    global selected_time
    disable_buttons()
    jokes = JOKES.get(selected_time, {}).get(joke_type, [])
    joke = random.choice(jokes) if jokes else f"No jokes available for this time and category, {user_name}."

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"Assistant: Here's a {joke_type} joke:\n{joke}\n\n")
    chat_log.config(state=tk.DISABLED)

    threading.Thread(target=speak, args=(joke,)).start()


def show_time_selection():
    """Displays the time selection menu."""
    # Clear existing buttons
    for widget in button_frame.winfo_children():
        widget.destroy()

    # Add time selection buttons
    for time in TIME_OPTIONS:
        tk.Button(button_frame, text=time, command=lambda t=time: handle_time_selection(t),
                  font=("Helvetica", scaled_font_size)).pack(side=tk.LEFT, padx=5)


def update_time():
    """Updates the current time label every second."""
    now = datetime.now(pytz.timezone("Europe/Bucharest"))
    time_label.config(text=f"Current Time: {now.strftime('%H:%M:%S')}")
    time_label.after(1000, update_time)


def start_app():
    """Stores the user's name and proceeds to the main application."""
    global user_name
    user_name = name_entry.get().strip()
    if user_name:
        # Remove the name entry frame and show the main app
        name_entry_frame.destroy()
        run_main_app()


def run_main_app():
    """Runs the main application."""
    global chat_log, button_frame, time_label

    # Chat log area
    chat_log = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD, bg="lightgray", fg="black",
                       font=("Helvetica", scaled_font_size))
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Add current time label
    time_label = tk.Label(root, text="", font=("Helvetica", scaled_font_size))
    time_label.pack(pady=5)
    update_time()  # Start updating the time

    # Button frame for interactive options
    button_frame = tk.Frame(root)
    button_frame.pack(padx=10, pady=5)

    # Show time selection buttons
    show_time_selection()


# Tkinter GUI for chatbot
def run_chatbot_gui():
    """Runs the chatbot application with a name entry."""
    global root, name_entry, name_entry_frame

    # Create the main window
    root = tk.Tk()
    root.title("Virtual Robot Assistant")

    # Name entry frame
    name_entry_frame = tk.Frame(root)
    name_entry_frame.pack(pady=20)

    tk.Label(name_entry_frame, text="Enter your name:", font=("Helvetica", scaled_font_size)).pack(side=tk.LEFT, padx=5)
    name_entry = tk.Entry(name_entry_frame, font=("Helvetica", scaled_font_size))
    name_entry.pack(side=tk.LEFT, padx=5)
    tk.Button(name_entry_frame, text="Start", command=start_app, font=("Helvetica", scaled_font_size)).pack(side=tk.LEFT,
                                                                                                            padx=5)

    # Run the main loop
    root.mainloop()


if __name__ == "__main__":
    run_chatbot_gui()
