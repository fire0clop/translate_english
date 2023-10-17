import math
import random
from mimesis import Generic

def random_choise(list_word):
    # Создайте список объектов и вероятностей
    objects = [translation for translation in list_word]
    probabilities = []

    # Вычислите вероятность для каждого объекта на основе значения progress с использованием логарифмической функции
    for translation in list_word:
        probability = 1 / math.exp(translation.progress)  # Используем логарифмическую функцию
        probabilities.append(probability)

    # Используйте random.choices() для выбора случайного объекта с учетом вероятности
    random_translation = random.choices(objects, weights=probabilities)[0]
    return random_translation
def generate_rus_word():
    # Создайте экземпляр Generic для русского языка
    random_list = []
    fake = Generic('ru')
    for _ in range(0,3):
        random_word = fake.text.word()
        random_list.append(random_word)
    return random_list