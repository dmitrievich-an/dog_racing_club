"""
1. Пользователь вводит количество кругов (1 круг = 400 метров, не менее 3-х кругов)
2. Пользователю выводится таблица с 8-ю участниками (номер участника, кличка, коэффициент, начальная скорость):
    2.1 Клички собак случайны (берутся из набора)
    2.2 Коэффициент ставки зависит от начальной скорости собаки (рандомное значение при "создании" собаки)
    2.3 С каждым пройденным кругом скорость собаки уменьшается на рандомное значение, но не может быть меньше 11
3. Пользователь вводит номер участника
4. Пользователь вводит сумму ставки
5. У пользователя изначально есть 10000$
    5.1 После каждого забега выводится сообщение о проигрыше или выигрыше и текущий (т.е. новый) баланс

Дополнительно:
1. При создании арены для забега можно указать погодные условия (по умолчанию сухо и солнечно)
2. Добавить возможность ставить сразу на несколько собак
3. Добавить проверку на вилку (общая сумма ставок на всех собак не может быть меньше минимального выигрыша)
"""
import random
import time
from operator import index


# Описываем арену
class Arena:
    def __init__(self, number_of_laps, weather=0):
        self.laps = number_of_laps
        self.length = 400
        self.weather = weather


# Описываем игрока
class Player:
    def __init__(self):
        self._money = 10000  # стартовый баланс

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, money):
        self._money = money


# Описываем собаку
class Dog:
    dog_names = [
        "Шарик",
        "Бобик",
        "Рекс",
        "Дружок",
        "Лайка",
        "Белка",
        "Стрелка",
        "Джек",
        "Лорд",
        "Чара",
        "Бим",
        "Жучка",
        "Тайсон",
        "Ричи",
        "Барон",
        "Граф",
        "Снупи",
        "Тузик",
        "Макс",
        "Боня"
    ]
    used_names = []

    def __init__(self):
        self.speed = random.randrange(280, 421) / 10
        self.odds = round(5.55 - self.speed / 10, 2)
        # TODO: Переписать на выдачу рандомной клички из списка незанятых (создать его)
        # Сейчас он тупо выдаст первые имена
        for name in Dog.dog_names:
            if name not in Dog.used_names:
                self.name = name
                Dog.used_names.append(name)
                break
        self.total_time = 0


# Функция начала игры
def start_game():
    # TODO Дописать проверку на целое положительное число от 3 до 10 (иначе собачки устанут)
    laps = int(input('Введите количество кругов: '))
    arena = Arena(laps)
    player = Player()
    dogs = [Dog() for i in range(1, 9)] # Создаем список из 8 песиков
    odds = [dogs[i].odds for i in range(len(dogs))] # Создаем массив коэффициентов для проверки на вилку

    # TODO: Описать поведение при наличии вилки, пока исходим из того, что она отсутствует
    is_fork = sum(1 / i for i in odds) # Проверка наличия вилки
    # print('есть вилка, пересчитать коэффициенты') if is_fork < 1 else print('вилки нет, можно продолжать')

    # Рисуем таблицу участников
    print('')
    print(f'{'Таблица участников':>25}')
    print('')
    print(f"{'№':<3} {'Имя':<10} {'Коэф.':<8} {'Нач. скор.':>10}")
    print('-' * 34)
    for idx, dog in enumerate(dogs, start=1):
        print(f"{idx:<3} {dog.name:<10} {dog.odds:<8} {dog.speed:>10}")
    print('')

    # Принимаем ставку
    winner = int(input('Введите номер участника для ставки: '))
    bet_amount = int(input('Введите сумму ставки: '))
    print(f'баланс: {player.money}')
    player.money -= bet_amount
    print(f'баланс: {player.money}')

    # Для красоты
    print('')
    print(f'Вы поставили {bet_amount}$ на победу участника №{winner} по кличке {dogs[winner - 1].name}')
    print('')
    print('Забег начинается!')
    text = "3...2...1..."
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.2)
    print('')
    print('')

    # Вычисляем победителя
    lap_winner = None
    current_lap = 1
    while current_lap <= arena.laps:
        for dog in dogs:
            dog.total_time += arena.length / dog.speed
            # Раскомментировать print ниже, чтобы отследить лидера по каждому кругу
            print(f'Текущая скорость: {dog.speed:.2f} Общее время: {dog.total_time:.3f} ')
            dog.speed -= round(random.randrange(10, 120) / 10, 2)
            if dog.speed < 11:
                dog.speed = 11
        arr_total_time = [dogs[i].total_time for i in range(len(dogs))]
        lap_winner = arr_total_time.index(min(arr_total_time))
        print(f'В конце {current_lap}го круга лидирует {dogs[lap_winner].name}')
        current_lap += 1
        time.sleep(1.5)
    print('')
    print(f'{dogs[lap_winner].name} - победитель!')

    # Вычисляем сумму выигрыша
    if dogs[lap_winner].name == dogs[winner - 1].name:
        print('Ваша ставка сыграла!')
        print(f'Сумма ставки: {bet_amount}. Выигрыш: {bet_amount * dogs[lap_winner].odds}')
        player.money += bet_amount * dogs[lap_winner].odds
    else:
        print('Ваша ставка не прошла. Возможно повезет в следующий раз!')
    print(f'Текущий баланс: {player.money}')


start_game()