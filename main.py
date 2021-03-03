from ChatBot import ChatBot
import settings
from tkinter import Tk, Button, Label, Entry, StringVar

def send_message(event):
    text = f"You:\n{input_message.get()}"
    current_text.set(text)


root = Tk()
current_text = StringVar()
root.geometry("1500x1500")
label = Label(root, text="Enter ur message", font=settings.main_font)
label.place(x=20, y=20)
input_message = Entry(root, font=settings.main_font)
input_message.place(x=20, y=80)
send_message_button = Button(root, text="Send message", font=settings.main_font)
send_message_button.place(x=20, y=160)
send_message_button.bind("<Button-1>", send_message)
chat_window = Label(root, font=settings.window_font, textvariable=current_text)
chat_window.place(x=800, y=20)
root.mainloop()