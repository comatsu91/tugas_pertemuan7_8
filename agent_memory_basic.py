from tools import kalkulator, kamus_lookup, baca_file

memory_chat = []  # list of dict: {"role": "...", "content": "..."}

def simpan_chat(role, content):
    memory_chat.append({"role": role, "content": content})

def tampilkan_ringkas_chat(n=5):
    return memory_chat[-n:]

def agent_jawab(user_input: str) -> str:
    teks = user_input.lower().strip()

    if "hitung" in teks:
        expr = teks.replace("hitung", "").strip()
        hasil = kalkulator(expr)
        return f"Hasil perhitungan: {hasil}"

    if teks.startswith("arti "):
        kata = teks.replace("arti", "").strip()
        hasil = kamus_lookup(kata)
        return f"Arti '{kata}': {hasil}"

    if teks.startswith("baca file "):
        path = teks.replace("baca file", "").strip()
        hasil = baca_file(path)
        return f"Isi file '{path}':\n{hasil}"

    if teks == "ringkas chat":
        ringkas = tampilkan_ringkas_chat()
        return f"Ringkasan chat terakhir: {ringkas}"

    return "Saya belum punya tool untuk itu. Coba: hitung / arti / baca file / ringkas chat."

while True:
    q = input("\nKamu: ")
    if q.lower() in ["exit", "quit"]:
        print("Agent berhenti.")
        break

    simpan_chat("user", q)
    ans = agent_jawab(q)
    simpan_chat("agent", ans)

    print("Agent:", ans)
    
import json

def save_memory(path="memory_chat.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory_chat, f, indent=2)

def load_memory(path="memory_chat.json"):
    global memory_chat
    try:
        with open(path, "r", encoding="utf-8") as f:
            memory_chat = json.load(f)
    except FileNotFoundError:
        memory_chat = []