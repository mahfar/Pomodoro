import math
from tkinter import *

from PIL import Image, ImageTk

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#1B9C85"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 10
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 25
SHORT_BREAK_SNOOZE = 1
COUNT_SNOOZE = 0
repeat = 0
timer = None


# -----------------------------Reset----------------------------- #
def exit_pomodoro():
    window.destroy()


# -----------------------------Reset----------------------------- #
def reset_timer():
    global repeat
    window.after_cancel(timer)
    title_label.config(text="")
    canvas.itemconfig(timer_text, text="00:00")
    check_marks.config(text="")
    repeat = 0


# -----------------------------Snooz----------------------------- #
def start_timer():
    global SHORT_BREAK_SNOOZE
    SHORT_BREAK_SNOOZE = 1
    global repeat
    repeat += 1
    if repeat % 8 == 0:
        title_label.config(text="25 min Break", fg=RED)
        count_down(LONG_BREAK_MIN * 60)
    elif repeat % 2 == 0:
        title_label.config(text="5 min Break", fg=PINK)
        count_down(SHORT_BREAK_MIN)
    else:
        title_label.config(text="Working!", fg=GREEN)
        count_down(WORK_MIN)


# -----------------------------Snooze----------------------------- #
def snooze_timer():
    global SHORT_BREAK_SNOOZE
    SHORT_BREAK_SNOOZE -= 1


# -----------------------------CountDown----------------------------- #
def count_down(count):
    global SHORT_BREAK_SNOOZE
    if SHORT_BREAK_SNOOZE == 0:
        count += 5
        SHORT_BREAK_SNOOZE = 1

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        session_mark_num = math.floor(repeat/2)
        for _ in range(session_mark_num):
            marks += "✔"
        check_marks.config(text=marks)


window = Tk()
window.title("Pomodoro")
window.config(pady=20, padx=20, bg=YELLOW)

title_label = Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 16))
title_label.grid(column=1, row=0)

check_marks = Label(fg=GREEN, bg=YELLOW, font=('Times', 16))
check_marks.grid(column=1, row=1)

canvas = Canvas(width=128, height=128, bg=YELLOW, highlightthickness=0)
tomato_img = Image.open("tomato.png")
tomato_resize_img = tomato_img.resize((128, 128))
tomato_img = ImageTk.PhotoImage(tomato_resize_img )
canvas.create_image(64, 64, image=tomato_img)
timer_text = canvas.create_text(64, 64, text="00:00", fill="white", font=(FONT_NAME, 26, "bold"))
canvas.grid(column=1, row=2)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.config(height=2, width=3, bd=0)
start_button.grid(column=0, row=3)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.config(height=2, width=3, bd=0)
reset_button.grid(column=1, row=3)

snooze_button = Button(text="+5Sec", highlightthickness=0, command=snooze_timer)
snooze_button.config(height=2, width=3, bd=0)
snooze_button.grid(column=2, row=3)

exit_button = Button(text="Exit", highlightthickness=0, command=exit_pomodoro)
exit_button.config(height=2, width=3, bd=0)
exit_button.grid(column=1, row=4, pady=9)




window.mainloop()

