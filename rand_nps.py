import random


class Rand_monster(object):

    def __init__(self, numrand):
        self.numrand = numrand
        if numrand == 0:
            monter = ["Гоблин", "Слизень", "Крыс"]
            self.rand_monster = random.choice(monter)
        elif numrand == 1:
            monter = ["Паук", "Гоблин", "Слизень", "Крыс", "Зараженный", "Зомби"]
            self.rand_monster = random.choice(monter)
        elif numrand == 2:
            monter = ["Песчанный Паук", "Песчанный Гоблин", "Песчанный Слизень", "Песчанный Крыс", "Песчанный Зомби"]
            self.rand_monster = random.choice(monter)
        elif numrand == 3:
            monter = ["Водный Паук", "Водный Гоблин", "Водный Слизень", "Водный Крыс", "Водный Зараженный",
                      "Водный Зомби"]
            self.rand_monster = random.choice(monter)
        elif numrand == 4:
            monter = ["Огненный Паук", "Огненный Гоблин", "Огненный Слизень", "Огненный Голем"]
            self.rand_monster = random.choice(monter)
        elif numrand == 5:
            monter = ["Ведьма", "Умертвие", "Скелет", "Мимик"]
            self.rand_monster = random.choice(monter)
        elif numrand == 6:
            monter = ["Рыба людоед", "Гоблин", "Сирена"]
            self.rand_monster = random.choice(monter)
        elif numrand == 7:
            monter = ["Кракен"]
            self.rand_monster = random.choice(monter)
        elif numrand == 8:
            monter = ["Дракон"]
            self.rand_monster = random.choice(monter)

    def get_rand_monster(self):
        return self.rand_monster
