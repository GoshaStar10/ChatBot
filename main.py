from ChatBot import ChatBot
from history import History
import settings
from tkinter import Tk, Button, Label, Entry, StringVar


def create_text():
    text = ""
    for i in range(len(history.user_messages)):
        text += f"You:\n{history.user_messages[i]}\n\n"
        text += f"CHATBOT:\n{history.bot_messages[i]}\n\n"
    return text


def send_message(event):
    our_message = input_message.get()
    history.add_our_message(our_message)
    history.add_bot_messages(bot.get_answer(our_message))
    current_text.set(create_text())


root = Tk()
current_text = StringVar()
root.geometry("1500x1500")
root.title("CHATBOT")
history = History()
bot = ChatBot()
input_message = Entry(root, font=settings.main_font)
input_message.place(x=20, y=80)
send_message_button = Button(root, text="Send message", font=settings.main_font)
send_message_button.place(x=20, y=160)
send_message_button.bind("<Button-1>", send_message)
label = Label(root,
              text="Enter your message",
              font=settings.window_font,
              bg=settings.chat_wordstring_bg,
              justify="left",
              anchor="nw")
chat_window = Label(root,
                    font=settings.window_font,
                    bg=settings.chat_window_bg,
                    height=26,
                    width=38,
                    justify="left",
                    anchor="nw",
                    wraplength=700,
                    textvariable=current_text)
chat_window.place(x=800, y=50)
label.place(x=20, y=20)
root.mainloop()
