from tkinter import Tk, Checkbutton, Button, Label, Entry, Text, Scrollbar, Y, RIGHT, INSERT, END, WORD, IntVar
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


def show_color_buttons(event):
    for i in range(len(color_buttons)):
        color_buttons[i].place(x=20+15*(i%4)*w, y=650+20*(i//4)*h)
    button_config.place(x=20, y=1000)
    label_config.place(x=170, y=1000)
    entry_config.place(x=320, y=1000)
    font_config.place(x=550, y=1000)
    close_settings_button.place(x=20, y=1100)


def hide_color_buttons(event):
    for i in range(len(color_buttons)):
        color_buttons[i].place(x=-100, y=-100)
    button_config.place(x=-100, y=-100)
    label_config.place(x=-100, y=-100)
    entry_config.place(x=-100, y=-100)
    font_config.place(x=-100, y=-100)
    close_settings_button.place(x=-100, y=-100)


def save_settings(parametr, value):
    file = open("settings.py", "r")
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        try:
            p, v = lines[i].split(" = ")
            if p == parametr:
                lines[i] = f'{parametr} = "{value}"\n'
        except:
            continue
    file = open("settings.py", "w")
    file.writelines(lines)
    file.close()


def change_color(event):
    color = event.widget.color
    if button_config_variable.get() == 1:
        send_message_button.config(bg=color)
        settings_button.config(bg=color)
        close_settings_button.config(bg=color)
        save_settings("button_color", color)
    if label_config_variable.get() == 2:
        label.config(bg=color)
        save_settings("chat_wordstring_bg", color)
    if entry_config_variable.get() == 3:
        input_message.config(bg=color)
        chat_window.config(bg=color)
        save_settings("chat_window_bg", color)
    if font_config_variable.get() == 4:
        send_message_button.config(fg=color)
        settings_button.config(fg=color)
        close_settings_button.config(fg=color)
        label.config(fg=color)
        input_message.config(fg=color)
        chat_window.config(fg=color)
        save_settings("font_color", color)

root = Tk()
root.geometry("2000x1500")
root.title("CHATBOT")
history = History()
bot = ChatBot()
input_message = Entry(root,
                      bg=settings.chat_window_bg,
                      fg=settings.font_color,
                      font=settings.main_font)
input_message.place(x=20, y=80)
send_message_button = Button(root,
                             text="Отправить сообщение",
                             fg=settings.font_color,
                             bg=settings.button_color,
                             font=settings.main_font)
send_message_button.place(x=20, y=160)
send_message_button.bind("<Button-1>", send_message)
label = Label(root,
              text="Введите ваше сообщение",
              font=settings.window_font,
              bg=settings.chat_wordstring_bg,
              fg=settings.font_color,
              justify="left",
              anchor="nw")
scroll = Scrollbar(root)
scroll.pack(side=RIGHT, fill=Y)
chat_window = Text(root,
                   font=settings.window_font,
                   bg=settings.chat_window_bg,
                   fg=settings.font_color,
                   height=26,
                   width=38,
                   wrap=WORD,
                   yscrollcommand=scroll.set)
chat_window.pack(side=RIGHT, fill=Y)
label.place(x=20, y=20)
settings_button = Button(root,
                         text="Настройки цвета",
                         fg=settings.font_color,
                         bg=settings.button_color,
                         font=settings.main_font)
settings_button.place(x=20, y=500)
settings_button.bind("<Button-1>", show_color_buttons)
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
    color_buttons[i].config(bg=settings.button_colors[i])
    color_buttons[i].color = settings.button_colors[i]
    color_buttons[i].bind("<Button-1>", change_color)
close_settings_button = Button(root,
                               text="Сохранить настройки цвета",
                               fg=settings.font_color,
                               bg=settings.button_color,
                               font=settings.main_font)
close_settings_button.bind("<Button-1>", hide_color_buttons)
button_config_variable = IntVar()
button_config = Checkbutton(root, text="Кнопки", variable=button_config_variable, \
                            onvalue=1, offvalue=0, height=1, width=5, font=settings.checkbox_font)
label_config_variable = IntVar()
label_config = Checkbutton(root, text="Метка", variable=label_config_variable, \
                            onvalue=2, offvalue=0, height=1, width=5, font=settings.checkbox_font)
entry_config_variable = IntVar()
entry_config = Checkbutton(root, text="Поле ввода", variable=entry_config_variable, \
                            onvalue=3, offvalue=0, height=1, width=10, font=settings.checkbox_font)
font_config_variable = IntVar()
font_config = Checkbutton(root, text="Шрифт", variable=font_config_variable, \
                            onvalue=4, offvalue=0, height=1, width=5, font=settings.checkbox_font)
root.mainloop()
