import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import threading
import time

user32 = ctypes.windll.user32
DOWN, UP = 0x0002, 0x0004

running = False
stop_event = threading.Event()

def click_once():
    user32.mouse_event(DOWN, 0, 0, 0, 0)
    user32.mouse_event(UP, 0, 0, 0, 0)

def worker():
    global running
    # Best-effort burst mode; Windows cannot guarantee exact 1 ms timing.
    while not stop_event.is_set():
        for _ in range(max(1, clicks_per_burst.get())):
            if stop_event.is_set():
                break
            click_once()
        time.sleep(max(0.000001, interval_ms.get() / 1000.0))
    running = False
    root.after(0, refresh)

def toggle():
    global running
    if running:
        stop_event.set()
        running = False
    else:
        stop_event.clear()
        running = True
        threading.Thread(target=worker, daemon=True).start()
    refresh()

def refresh():
    status.config(text="● RUNNING" if running else "● STOPPED")
    status.configure(foreground="#20d080" if running else "#ff5c5c")
    button.config(text="STOP" if running else "START")

def quit_app():
    stop_event.set()
    root.destroy()

root = tk.Tk()
root.title("Twin AutoClicker")
root.geometry("520x390")
root.resizable(False, False)
root.configure(bg="#101218")

clicks_per_burst = tk.IntVar(value=10)
interval_ms = tk.DoubleVar(value=1.0)

title = tk.Label(root, text="TWIN AUTOCLICKER", font=("Segoe UI", 22, "bold"),
                 bg="#101218", fg="white")
title.pack(pady=(22, 3))

tk.Label(root, text="High-speed burst clicker • F6 = Start/Stop • F7 = Exit",
         font=("Segoe UI", 10), bg="#101218", fg="#aab0bd").pack()

status = tk.Label(root, text="● STOPPED", font=("Segoe UI", 12, "bold"),
                  bg="#101218", fg="#ff5c5c")
status.pack(pady=15)

frame = tk.Frame(root, bg="#171a22")
frame.pack(padx=30, fill="x")

tk.Label(frame, text="Clicks per burst", bg="#171a22", fg="white",
         font=("Segoe UI", 10)).grid(row=0, column=0, padx=15, pady=15, sticky="w")
ttk.Spinbox(frame, from_=1, to=1000, textvariable=clicks_per_burst, width=12).grid(
    row=0, column=1, padx=15, pady=15)

tk.Label(frame, text="Interval (ms)", bg="#171a22", fg="white",
         font=("Segoe UI", 10)).grid(row=1, column=0, padx=15, pady=15, sticky="w")
ttk.Spinbox(frame, from_=0.001, to=1000, increment=0.001,
            textvariable=interval_ms, width=12).grid(row=1, column=1, padx=15, pady=15)

button = tk.Button(root, text="START", command=toggle, width=18, height=2,
                   bg="#2b72ff", fg="white", activebackground="#1859d1",
                   activeforeground="white", relief="flat", font=("Segoe UI", 12, "bold"))
button.pack(pady=20)

tk.Label(root, text="Watermark: KALRAV 726", font=("Segoe UI", 9, "bold"),
         bg="#101218", fg="#777d8a").pack(side="bottom", pady=10)

def hotkeys():
    import keyboard
    keyboard.add_hotkey("f6", lambda: root.after(0, toggle))
    keyboard.add_hotkey("f7", lambda: root.after(0, quit_app))
    keyboard.wait()

threading.Thread(target=hotkeys, daemon=True).start()
root.protocol("WM_DELETE_WINDOW", quit_app)
root.mainloop()
