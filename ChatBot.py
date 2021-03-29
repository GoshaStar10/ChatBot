from datetime import datetime
from random import randint

from bs4 import BeautifulSoup
from requests import get


class ChatBot():
    openweatherkey = "9979899419251cc17ec83e1aaa98ef8f"

    urls = {"SPA": "https://football.kulichki.net/spain/",
            "ENG": "https://football.kulichki.net/england/"}

    keywords = {"greetings": ["HELLO", "HI", "WHAT'S UP", "HEYO", "SUP"],
                "questions": ["?", "HOW", "WHERE", "WHEN", "WHAT", "WHO"],
                "weather": ["WEATHER", "COLD", "HOT", "WINDY", "TEMPERATURE", "OVERCAST", "GUSTY"],
                "time": ["TIME", "CLOCK", "HOUR", "MINUTE", "SECOND"],
                "mood": ["ARE YOU", "DO YOU DO", "IS IT GOING", "ARE YOU DOING", "MOOD"],
                "color": ["COLOUR", "COLOR", "SHADE", "TINT", "TONE", "TINGE"],
                "football": ["ФУТБОЛ"],
                "teams": [],
                "championships": ["BUNDESLIGA", "BUNDES", "GERMAN", "BPL", "PL", "ENGLISH", "SERIE A", "ITALIAN", "LIGUE 1", "FRENCH", "LA LIGA", "SPANISH", "RUSSIAN"]
                }

    answers = {"greetings": ["Hello!", "Hi", "Yo", "Sup", "Ey"],
               "questions": ["What championship would you like to see?"],
               "weather": ["It's cold today", "It's hot today", "It's windy today", "Today's temperature is alright ", "It's overcast today", "It's gusty today"],
               "mood": ["I feel good, thank u", "I feel bad ;((", "Nasty bro", "Cool, thx", "I feel sick", "Absolutely awesome"],
               "color": ["I enjoy light blue", "Pure white sounds nice, huh?", "Green, the same as the grass have", "Yellow is not a bad option at all!"],
               "championships": ["Wait a minute! I'm opening the desired line."]
               }

    football_table = {}

    football_terms = {"ПОЗИЦИЯ": "position",
                      "ИГРЫ": "position",
                      "ОЧКИ": "position",
                      "ПОБЕДЫ": "position",
                      "НИЧЬИ": "position",
                      "ПОРАЖЕНИЯ": "position",
                      "ГОЛЫ": "position"}

    def parse_site(self, url):
        soup = BeautifulSoup(get(url).text, "html.parser")
        table = soup.findAll("td", bgcolor="#cffccd")
        table = list(map(str, table))
        teams = {}
        for i in range(0, len(table), 7):
            team = table[i][table[i].find("htm")+5:table[i].find("</a>")]
            games = table[i + 1][table[i + 1].find("font size") + 14:table[i + 1].find("</font>")]
            wins = table[i + 2][table[i + 2].find("font size") + 14:table[i + 2].find("</font>")]
            draws = table[i + 3][table[i + 3].find("font size") + 14:table[i + 3].find("</font>")]
            loses = table[i + 4][table[i + 4].find("font size") + 14:table[i + 4].find("</font>")]
            goal_difference = table[i + 5][table[i + 5].find("font size") + 14:table[i + 5].find("</font>")]
            points = table[i + 6][table[i + 6].find("<b>") + 3:table[i + 6].find("</b>")]
            teams[i // 7 + 1] = {"team": team,
                                 "games": games,
                                 "wins": wins,
                                 "draws": draws,
                                 "loses": loses,
                                 "goal_difference": goal_difference,
                                 "points": points}
        self.football_table = teams

    def get_weather(self):
        city = "Saint Petersburg, RU"
        try:
            rqst = get("http://api.openweathermap.org/data/2.5/find", params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': self.openweatherkey})
            result = rqst.json()["list"][0]
            temperature_real = result["main"]["temp"]
            temperature_feel = result["main"]["feels_like"]
            pressure = result["main"]["pressure"]
            humidity = result["main"]["humidity"]
            wind_speed = result["wind"]["speed"]
            rain = "There is no rain now." if result["rain"] == None else "Rainy."
            description = result["weather"][0]["description"].capitalize()
            weather = f"Now in {city} is {temperature_real} degrees (but feels like {temperature_feel}). Pressure is " \
                      f"{pressure} Pa. Humidity is {humidity}%. Wind speed is {wind_speed} m/s. {rain} {description}."
            return weather
        except:
            return "Я не знаю:( Спроси меня позже!"

    def get_info(self, team):
        team = team.capitalize()
        try:
            position = 1
            while self.football_table[position]["team"] != team:
                position += 1
            return f"Команда {self.football_table[position]['team']}" \
                   f" идет на {position} месте. " \
                   f"Сыграла {self.football_table[position]['games']} матчей. " \
                   f"Побед: {self.football_table[position]['wins']}, " \
                   f"ничьи: {self.football_table[position]['draws']}, " \
                   f"поражения: {self.football_table[position]['loses']}. " \
                   f"Набрала {self.football_table[position]['points']} очков. " \
                   f"Разница забитых и пропущенных голов {self.football_table[position]['goal_difference']}."
        except:
            return "Я не знаю:( Спроси меня позже!"

    def set_teams(self):
        try:
            for key in self.football_table.keys():
                self.keywords["teams"].append(self.football_table[key]["team"].upper())
        except:
            return "Я не знаю:( Спроси меня позже!"

    def get_teams(self):
        text = "Я могу рассказать про команды: "
        for team in self.keywords["teams"]:
            text += team.capitalize() + ", "
        text += '.'
        return text


    def clear_text(self, text):
        new_text = ""
        for symbol in text:
            if symbol.isalnum() or symbol == ' ':
                new_text += symbol
        return new_text

    def get_answer(self, text):
        keys = set()
        text = self.clear_text(text.upper()).split()
        for key in self.keywords.keys():
            for word in text:
                if word in self.keywords[key]:
                    keys.add(key)
        answer = ""
        print(keys)
        if "time" in keys:
            return datetime.now().strftime("It's %H:%M:%S now.")
        elif "weather" in keys:
            return self.get_weather()
        elif "football" in keys:
            self.parse_site(self.urls["SPA"])
            self.set_teams()
            return self.get_teams()
        elif "teams" in keys:
            return self.get_info(text[0])
        else:
            for key in keys:
                answer += self.answers[key][randint(0, len(self.answers[key])) - 1] + '\n'
        print(keys)
        return answer
