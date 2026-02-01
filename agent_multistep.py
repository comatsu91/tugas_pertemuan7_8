import json
import os

def read_file(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return f.readlines()

def extract_points(lines, max_points=3):
    points = []
    for line in lines:
        line = line.strip()
        if line and len(points) < max_points:
            points.append(line)
    return points

def generate_quiz(points):
    quiz = []
    for i, point in enumerate(points, start=1):
        question = {
            "question": f"Apa inti dari pernyataan berikut?\n'{point}'",
            "options": [
                "Penjelasan yang benar",
                "Penjelasan salah A",
                "Penjelasan salah B",
                "Penjelasan salah C"
            ],
            "answer": "Penjelasan yang benar"
        }
        quiz.append(question)
    return quiz

def buat_quiz_dari_file(filename):
    print("[TRACE] Membaca file...")
    lines = read_file(filename)
    if lines is None:
        return "File tidak ditemukan."

    print("[TRACE] Mengambil 3 poin utama...")
    points = extract_points(lines)

    print("[TRACE] Membuat soal quiz...")
    quiz = generate_quiz(points)

    output = ""
    for i, q in enumerate(quiz, start=1):
        output += f"\nSoal {i}: {q['question']}\n"
        for opt in q["options"]:
            output += f"- {opt}\n"
    return output

if __name__ == "__main__":
    command = input("Masukkan perintah: ")

    if command.startswith("buat quiz dari file"):
        filename = command.replace("buat quiz dari file", "").strip()
        result = buat_quiz_dari_file(filename)
        print(result)
