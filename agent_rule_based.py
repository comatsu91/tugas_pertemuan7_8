# agent_rule_based.py
import sys
from tools import (
    convert_temperature,
    calculate_bmi,
    search_word_in_file,
    most_frequent_word
)

def agent(command):
    command = command.lower().split()

    if "konversi" in command and "suhu" in command:
        # contoh: konversi suhu 30 C
        value = float(command[-2])
        unit = command[-1].upper()
        print("Hasil konversi:", convert_temperature(value, unit))

    elif "bmi" in command:
        # contoh: bmi 70 1.7
        weight = float(command[-2])
        height = float(command[-1])
        print("Nilai BMI:", calculate_bmi(weight, height))

    elif "cari" in command and "kata" in command:
        # contoh: cari kata data.txt python
        filename = command[-2]
        word = command[-1]
        print(f"Kata '{word}' muncul sebanyak",
              search_word_in_file(filename, word), "kali")

    elif "kata" in command and "terbanyak" in command:
        # contoh: kata terbanyak data.txt
        filename = command[-1]
        print("Kata paling sering muncul:",
              most_frequent_word(filename))

    else:
        print("Perintah tidak dikenali")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gunakan 1 perintah langsung")
        print("Contoh:")
        print('python agent_rule_based.py "bmi 70 1.7"')
    else:
        agent(" ".join(sys.argv[1:]))
