from tools import (kalkulator, kamus_lookup, baca_file, 
                   konversi_suhu, hitung_bmi, hitung_kata_file)
from datetime import datetime
import json
import re

# --- FITUR MEMORY ---
memory_chat = []

def save_memory(path="memory_chat.json"):
    """Menyimpan memori chat ke file JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory_chat, f, indent=2)

def load_memory(path="memory_chat.json"):
    """Memuat memori chat dari file JSON."""
    global memory_chat
    try:
        with open(path, "r", encoding="utf-8") as f:
            memory_chat = json.load(f)
    except FileNotFoundError:
        memory_chat = []

def simpan_chat(role, content):
    """Menambah chat ke list memori."""
    memory_chat.append({"role": role, "content": content})
    # Langsung save setiap ada chat baru agar aman jika program crash
    save_memory()

def format_ringkas_chat(n=5):
    """Merapikan tampilan ringkasan chat agar mudah dibaca."""
    chats = memory_chat[-n:]
    if not chats: return "Belum ada riwayat percakapan."
    
    hasil = "\n--- 5 Pesan Terakhir ---\n"
    for c in chats:
        sender = "Anda" if c['role'] == "user" else "Agent"
        hasil += f"{sender}: {c['content']}\n"
    return hasil

# --- LOGIKA AGENT ---
def log_interaksi(user_input, agent_output):
    """Mencatat ke log_agent.txt (Format teks untuk dosen)."""
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_agent.txt", "a", encoding="utf-8") as f:
        f.write(f"[{waktu}]\nUSER : {user_input}\nAGENT: {agent_output}\n{'-'*30}\n")

def agent_jawab(user_input: str) -> str:
    teks = user_input.lower().strip()

    # 1. Ringkas Chat (Memory Tool)
    if teks == "ringkas chat":
        return format_ringkas_chat()

    # 2. Otomatis: Kalkulator
    if any(c.isdigit() for c in teks) and any(op in teks for op in "+-*/"):
        if "bmi" not in teks and "suhu" not in teks:
            return f"Hasil: {kalkulator(teks)}"

    # 3. Rule: BMI
    if "bmi" in teks:
        angka = re.findall(r"\d+", teks)
        if len(angka) >= 2:
            return hitung_bmi(float(angka[0]), float(angka[1]))
        return "Gunakan: bmi [berat] [tinggi]"

    # 4. Rule: Suhu
    if "suhu" in teks:
        match = re.search(r"(\d+).+ke\s+([cf])", teks)
        if match: return konversi_suhu(float(match.group(1)), match.group(2))

    # 5. Rule: Cari Kata
    if "cari" in teks and " di " in teks:
        parts = teks.replace("cari", "").split(" di ")
        return hitung_kata_file(parts[1].strip(), parts[0].strip())

    # 6. Rule: Kamus & Baca File
    if "arti" in teks: return kamus_lookup(teks.replace("arti", "").strip())
    if "baca" in teks: return baca_file(teks.replace("baca", "").replace("file", "").strip())

    return "Maaf, coba gunakan: hitung, bmi, suhu, arti, baca file, atau ringkas chat."

# --- MAIN LOOP ---
def main():
    load_memory() # Muat memori saat program dijalankan
    print("=== Agent Aktif (Memory System Enabled) ===")
    print("Ketik 'exit' untuk berhenti.")

    try:
        while True:
            q = input("\nKamu: ")
            if not q.strip(): continue
            if q.lower() in ["exit", "quit"]:
                print("Agent: Sampai jumpa! Memori tersimpan.")
                break

            # Simpan input user ke memori
            simpan_chat("user", q)
            
            ans = agent_jawab(q)
            print("Agent:", ans)
            
            # Simpan jawaban agent ke memori
            simpan_chat("agent", ans)
            
            # Tetap catat ke log_agent.txt sesuai tugas dosen
            log_interaksi(q, ans)
            
    except KeyboardInterrupt:
        save_memory()
        print("\nAgent berhenti secara paksa.")

if __name__ == "__main__":
    main()