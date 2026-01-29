from tkinter import *
import tkinter as tk

app = tk.Tk()
app.tk.call('tk', 'scaling', 2.0)

app.geometry("800x450")
app.title("CleanMyKeyboard")

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)
app.columnconfigure(2, weight=1)

app.rowconfigure(0, weight=1)
app.rowconfigure(1, weight=1)
app.rowconfigure(2, weight=1)

StartStop = tk.Button(app,
                   text='Start',
                   bg='red',
                   relief='flat',
                   width=60,
                   height=2
                   )

StartStop.grid(
    row=2,
    column=1,
)

app.mainloop()