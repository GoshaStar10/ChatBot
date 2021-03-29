class History:
    user_messages = []
    bot_messages = []

    def add_our_message(self, text):
        self.user_messages.append(text)

    def add_bot_messages(self, text):
        self.bot_messages.append(text)

