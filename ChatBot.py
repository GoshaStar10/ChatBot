from datetime import datetime
from random import randint
from bs4 import BeautifulSoup
from requests import get
from googlesearch import search


class ChatBot():
    openweatherkey = "9979899419251cc17ec83e1aaa98ef8f"

    urls = {"SPA": "https://football.kulichki.net/spain/",
            "ENG": "https://football.kulichki.net/england/",
            "GER": "https://football.kulichki.net/germany/",
            "ITA": "https://football.kulichki.net/italy/",
            "FRA": "https://football.kulichki.net/france/",
            "NED": "https://football.kulichki.net/holland/",
            "POR": "https://football.kulichki.net/portugal/",
            "TUR": "https://football.kulichki.net/turkey/",
            "RUS": "https://football.kulichki.net/ruschamp/"}

    countries = {"ИСПАНИЯ": "SPA", "АНГЛИЯ": "ENG", "ГЕРМАНИЯ": "GER", "ИТАЛИЯ": "ITA", "ФРАНЦИЯ": "FRA",
                 "НИДЕРЛАНДЫ": "NED", "ГОЛЛАНДИЯ": "NED", "ПОРТУГАЛИЯ": "POR", "ТУРЦИЯ": "TUR", "РОССИЯ": "RUS"}

    keywords = {"greetings": ["ЗДРАВСТВУЙТЕ", "ПРИВЕТ", "ХАЙ", "САЛЮТ"],
                "questions": ["?", "КАК", "КОГДА", "ГДЕ", "ЧТО", "КТО"],
                "weather": ["ПОГОДА", "ХОЛОДНО", "ЖАРКО", "ВЕТРЕНО", "ТЕМПЕРАТУРА", "ПАСМУРНО", "ОБЛАЧНО"],
                "time": ["ВРЕМЯ", "ЧАСЫ", "ЧАС", "МИНУТА", "СЕКУНДА"],
                "mood": ["ДЕЛА", "НАСТРОЕНИЕ", "ПРОШЁЛ ТВОЙ ДЕНЬ", "ЖИЗНЬ"],
                "color": ["ЦВЕТ", "ОТТЕНОК"],
                "football": ["ФУТБОЛ"],
                "countries": ["ИСПАНИЯ", "АНГЛИЯ", "ГЕРМАНИЯ", "ИТАЛИЯ", "ФРАНЦИЯ", "ПОРТУГАЛИЯ",
                              "НИДЕРЛАНДЫ", "ГОЛЛАНДИЯ", "РОССИЯ", "ТУРЦИЯ"],
                "teams": []
                }

    answers = {"greetings": ["Привет!", "Салют", "Йоу", "Здравствуй", "Доброго времени суток!"],
               "questions": ["Чемпионат какой страны Вас интересует?"],
               "weather": ["Сегодня прохладно", "Сегодня очень жарко", "На улице ветрено", "На улице вполне комфортная температура", "Сегодня пасмурно", "Облачно"],
               "mood": ["Я чувствую себя прекрасно, спасибо!", "Если честно, так себе;((", "Настроение просто супер!", "Клёво!", "Просто великолепно!"],
               "color": ["Мне нравится светло-голубой", "Ярко-жёлтый выглядит отлично, да?", "Зелёный, как у травы", "Лимонный цвет выглядит потрясающе!"],
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
                   f" идет на {position} месте, приняв участие " \
                   f"в {self.football_table[position]['games']} матчах,: " \
                   f"в {self.football_table[position]['wins']} из которых она одержала победу, " \
                   f"в {self.football_table[position]['draws']} команды разошлись с миром, " \
                   f"а в {self.football_table[position]['loses']} матчах уезжала без изменений в графе очков. " \
                   f"Итого, команда {self.football_table[position]['team']} имеет в своём активе {self.football_table[position]['points']} очков. " \
                   f"Разница забитых и пропущенных равняется {self.football_table[position]['goal_difference']}."
        except:
            return "Я не знаю:( Спроси меня позже!"

    def team_text(self, text):
        words = text.split()
        result = ""
        for i in range(len(words)):
            if words[i] == "ПСВ" or words[i] == "ПСЖ" or words[i] == "II" or words[i] == "Сент-Этьен" or words[i] == "АЗ" or words[i] == "РКС" or words[i] == "ВВВ" or words[i] == "АДО" or words[i] == "ЦСКА":
                result += words[i]
            else:
                result += words[i].capitalize() + " "
        result = result.rstrip()
        return result


    def set_teams(self):
        self.keywords["teams"] = []
        try:
            for key in self.football_table.keys():
                self.keywords["teams"].append(self.football_table[key]["team"].upper())
        except:
            return "Я не знаю:( Спроси меня позже!"

    def get_teams(self):
        text = "Я могу рассказать про команды: "
        for team in self.keywords["teams"]:
            text += self.team_text(team) + ", "
        text = text[:-2] + "."
        return text

    def get_links(self, text):
        links = ""
        for link in search(str(text), num_results=5, lang="ru"):
            links += link + "\n"
        return "Я не знаю ответа на этот вопрос, но Вы можете посмотреть, что по этому поводу пишут в интернете:\n" + links

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
            return "Я могу рассказать про чемпионаты Испании, " \
                   "Англии, Германии, Италии, Франции, Португалии, " \
                   "Нидерландов (Голландии), России, Турции. Чемпионат какой страны Вас интересует?"
        elif "countries" in keys:
            self.parse_site(self.urls[self.countries[text[0]]])
            self.set_teams()
            return self.get_teams()
        elif "teams" in keys:
            return self.get_info(text[0])
        elif len(keys) == 0:
            return self.get_links(text)
        else:
            for key in keys:
                answer += self.answers[key][randint(0, len(self.answers[key])) - 1] + '\n'
        print(keys)
        return answer
