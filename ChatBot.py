class ChatBot():
    keywords = {"greetings": ["HELLO", "HI", "HEY"],
                "questions": ["?", "HOW", "WHERE", "WHEN", "WHY", "WHAT", "WHO"]}

     def __init__(self, type, name):
            self.type = type
            self.name = name
            
     def get_request(self, text):
        sentences = list(text.split("."))
        types = set()
        for words in sentences:
            words = words.split()
            for word in words:
                word = word.upper()
                for current_type in ChatBot.keywords.keys():
                    if word in ChatBot.keywords[current_type]:
                        types.add(current_type)
                       
        return types
