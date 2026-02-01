# tools.py
from collections import Counter

def convert_temperature(value, from_unit):
    if from_unit.upper() == 'C':
        return (value * 9/5) + 32
    elif from_unit.upper() == 'F':
        return (value - 32) * 5/9
    else:
        raise ValueError("Unit harus 'C' atau 'F'")

def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def search_word_in_file(filename, word):
    count = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            count += line.lower().count(word.lower())
    return count

def most_frequent_word(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        words = f.read().lower().split()
    return Counter(words).most_common(1)
