from tkinter import Tk, Canvas, Button, Label, Entry, Text, Scrollbar, Y, RIGHT, INSERT, END
import settings
from ChatBot import ChatBot
from history import History


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
    chat_window.delete("1.0", END)
    chat_window.insert(INSERT, create_text())


def change_color(event):
    send_message_button.config(bg="#7FFFD4")


root = Tk()
root.geometry("1500x1500")
root.title("CHATBOT")
history = History()
bot = ChatBot()
input_message = Entry(root, font=settings.main_font)
input_message.place(x=20, y=80)
send_message_button = Button(root, text="Отправить сообщение", font=settings.main_font)
send_message_button.place(x=20, y=160)
send_message_button.bind("<Button-1>", send_message)
label = Label(root,
              text="Введите ваше сообщение",
              font=settings.window_font,
              bg=settings.chat_wordstring_bg,
              justify="left",
              anchor="nw")
scroll = Scrollbar(root)
scroll.pack(side=RIGHT, fill=Y)
chat_window = Text(root,
                   font=settings.window_font,
                   bg=settings.chat_window_bg,
                   height=26,
                   width=38,
                   yscrollcommand=scroll.set)
chat_window.pack(side=RIGHT, fill=Y)
label.place(x=20, y=20)
settings_button = Button(root, text="Настройки цвета", font=settings.main_font)
settings_button.place(x=20, y=500)
settings_button.bind("<Button-1>", change_color)
h, w = 5, 10
color_buttons = list()
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
color_buttons.append(Button(root, height=h, width=w))
for i in range(len(color_buttons)):
    color_buttons[i].place(x=20+15*(i%4)*w, y=650+20*(i//4)*h)
    color_buttons[i].config(bg=settings.button_colors[i])
    color_buttons[i].color = settings.button_colors[i]
root.mainloop()
