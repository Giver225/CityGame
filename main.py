from GUI import *

check_list = []


# Приводим название города в общий вид
def normalize_city_name(name):
    return name.strip().lower().replace('ё', 'е')


# Декоратор check_point, с его помощью регистрируем любые нужные нам методы, как методы проверки города от пользователя
def check_point(fun):
    check_list.append(fun)
    return fun


# Проверка, что город начинается с нужной буквы
@check_point
def is_city_startswith_char(city, char, **kwargs):
    if char is None or city.startswith(char):
        return True
    else:
        print(f'Город должен начинаться с буквы {char.capitalize()}.')
        return False


# Проверка, что город ещё не был назван
@check_point
def is_non_cached(city, cache, **kwargs):
    if city not in cache:
        return True
    else:
        print("Этот город уже был назван.")
        return False


# Проверка, что такой город существует и он известен нам
@check_point
def is_available(city, cities, **kwargs):
    if city in cities:
        return True
    else:
        print("Такого города не существует в России")
        return False


def move_to_cache(city, cities, cache):
    # Убираем из списка доступных городов
    cities.remove(city)
    # Перекидываем город в кэш
    cache.add(city)


def get_next_char(city):
    wrong_char = ("ъ", "ь", "ы", "й")
    # Выбираем букву для следующего города
    for char in city[::-1]:
        if char in wrong_char:
            continue
        else:
            break
    else:
        raise RuntimeError
    return char

# ход игрока, возвращает либо город, либо код ошибки
def user_point(char:str, cache:set, user_say:str, cities:set):
    city = normalize_city_name(user_say)
    kw = {"char": char, "cache": cache, "cities": cities}
    result_list = [x(city, **kw) for x in check_list]
    if not result_list[0]:
        return 0
    elif not result_list[1]:
        return 1
    elif not result_list[2]:
        return 2
    return city

def main():
    MyApp().run()



if __name__ == '__main__':
    # cache = set()
    # cities = {normalize_city_name(x) for x in open("cities.txt", "r").readlines() if x.strip()}
    main()
