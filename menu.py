import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def start_game():
    # Replace 'main.py' with the path to your game script if it's in a different directory
    try:
        subprocess.Popen(["python", "pong.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start the game: {e}")

def quit_game():
    root.destroy()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Kian's Powerful, Deadly Pong")

# Set the window size
root.geometry("300x200")

# Create the Start button
start_button = tk.Button(root, text="Start Game", command=start_game, font=("Helvetica", 14))
start_button.pack(pady=20)

# Create the Quit button
quit_button = tk.Button(root, text="Quit", command=quit_game, font=("Helvetica", 14))
quit_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
