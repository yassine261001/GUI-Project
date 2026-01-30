import tkinter as tk
from tkmacosx import Button
import threading
import Quartz
from Cocoa import CFRunLoopRun, CFRunLoopStop, CFRunLoopGetCurrent

app = tk.Tk()
app.geometry("800x450")
app.title("CleanMyKeyboard")
app.resizable(False, False)

# Grid config
for col in range(3):
    app.columnconfigure(col, weight=1)

for row in range(4):
    app.rowconfigure(row, weight=1)

Title = tk.Label(
    app,
    text="CleanMyKeyboard",
    font=("Helvetica", 28, "bold")
)
Title.grid(row=0, column=1, pady=(30, 10))

Description = tk.Label(
    app,
    text="Secure your keyboard while cleaning.\nClick Start to lock it.",
    font=("Helvetica", 14),
    wraplength=600,
    justify="center"
)
Description.grid(row=1, column=1, pady=10)

keyboard_thread = None
run_loop = None
tap = None
keyboard_active = False


def keyboard_callback(proxy, event_type, event, refcon):
    if event_type in (
        Quartz.kCGEventKeyDown,
        Quartz.kCGEventKeyUp
    ):
        return None  # BLOCK key
    return event


def start_keyboard_block():
    global tap, run_loop

    event_mask = (
        Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown) |
        Quartz.CGEventMaskBit(Quartz.kCGEventKeyUp)
    )

    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        Quartz.kCGHeadInsertEventTap,
        Quartz.kCGEventTapOptionDefault,
        event_mask,
        keyboard_callback,
        None
    )

    run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    run_loop = CFRunLoopGetCurrent()

    Quartz.CFRunLoopAddSource(
        run_loop,
        run_loop_source,
        Quartz.kCFRunLoopCommonModes
    )

    Quartz.CGEventTapEnable(tap, True)
    CFRunLoopRun()


def stop_keyboard_block():
    global run_loop, tap
    if run_loop:
        CFRunLoopStop(run_loop)
    if tap:
        Quartz.CGEventTapEnable(tap, False)


def activateApp():
    global keyboard_active, keyboard_thread

    if not keyboard_active:
        keyboard_thread = threading.Thread(
            target=start_keyboard_block,
            daemon=True
        )
        keyboard_thread.start()

        StartStop.config(
            text="Stop",
            bg="#e74c3c",
            activebackground="#e74c3c"
        )

        Description.config(
            text="Keyboard is deactivated.\nYou can safely clean it.\nClick Stop to reactivate."
        )

        keyboard_active = True

    else:
        stop_keyboard_block()

        StartStop.config(
            text="Start",
            bg="#2ecc71",
            activebackground="#2ecc71"
        )

        Description.config(
            text="Secure your keyboard while cleaning.\nClick Start to lock it."
        )

        keyboard_active = False


StartStop = Button(
    app,
    text="Start",
    bg="#2ecc71",
    fg="white",
    activebackground="#2ecc71",
    borderless=True,
    font=("Helvetica", 18, "bold"),
    width=220,
    height=60,
    command=activateApp
)

StartStop.grid(row=2, column=1, pady=40)

app.mainloop()
