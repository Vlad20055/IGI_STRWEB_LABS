import datetime as dt
import csv
import pickle


class Friend:
    def __init__(self, surname, name, patronymic, day, month, year):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.birthday = dt.date(year=year, month=month, day=day)

    def __str__(self):
        return f"{self.surname}, {self.name}, {self.patronymic}, Birthday: {self.birthday.strftime("%d/%m/%y")}"


class Data_service:
    data = [
        dict(surname = "Белоусов", name = "Антон", patronymic = "Дмитриевич", day = 12, month = 8, year = 2006),
        dict(surname = "Могилевец", name = "Денис", patronymic = "Эдуардович", day = 5, month = 4, year = 2006),
        dict(surname = "Любашенко", name = "Андрей", patronymic = "Сергеевич", day = 10, month = 4, year = 2006),
        dict(surname = "Ратников", name = "Ярослав", patronymic = "Дмитриевич", day = 17, month = 9, year = 2005),
        dict(surname = "Зорько", name = "Матвей", patronymic = "Юрьевич", day = 3, month = 1, year = 2005),
        dict(surname = "Лукьянов", name = "Степан", patronymic = "Владимирович", day = 11, month = 4, year = 2005)
    ]

    def serialize_csv(self):
        try:
            with open("Task1/Task1.csv", "w") as f:
                writer = csv.DictWriter(f, fieldnames=["surname", "name", "patronymic", "day", "month", "year"])
                writer.writeheader()
                writer.writerows(self.data)
        except Exception as e:
            print("Something went wrong", e)

    def serialize_pickle(self):
        try:
            with open("Task1/Task1.txt", "wb") as f:
                for el in self.data:
                    pickle.dump(el, f)
        except Exception as e:
            print("Something went wrong", e)

    def get_csv(self, old: int):
        try:
            with open("Task1/Task1.csv", "r") as f:
                reader = csv.DictReader(f)
                friends = []
                target_friends = []
                for row in reader:
                    friends.append(
                        Friend(row["surname"], 
                               row["name"],
                               row["patronymic"],
                               int(row["day"]),
                               int(row["month"]),
                               int(row["year"]))
                    )
        except Exception as e:
            print("Something went wrong!", e)

        for friend in friends:
            if (dt.date.today().year - friend.birthday.year) == old:
                target_friends.append(friend)
        return target_friends
        

    def get_pickle(self, old: int):
        try:
            with open("Task1/Task1.txt", "rb") as f:
                friends = []

                while True:
                    try:
                        data = pickle.load(f)
                        
                        friend = Friend(
                            surname=data["surname"],
                            name=data["name"],
                            patronymic=data["patronymic"],
                            day=data["day"],
                            month=data["month"],
                            year=data["year"]
                        )
                        friends.append(friend)
                    except EOFError:
                        break
        except Exception as e:
            print(f"Something went wrong: {e}")

        result = []
        for friend in friends:
            if (dt.date.today().year - int(friend.birthday.year)) == old:
                result.append(friend)
        return result
        


ds = Data_service()
ds.serialize_csv()
ds.serialize_pickle()
        