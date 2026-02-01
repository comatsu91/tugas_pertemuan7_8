from tools import (kalkulator, kamus_lookup, baca_file, 
                   konversi_suhu, hitung_bmi, hitung_kata_file)
from datetime import datetime
import json
import re
import os

# --- 1. FITUR MEMORY & TASK LIST ---
memory_chat = []

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

def simpan_chat(role, content):
    memory_chat.append({"role": role, "content": content})
    save_memory()

# --- 2. FUNGSI LOGGING ---
def log_interaksi(user_input, agent_output):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_agent.txt", "a", encoding="utf-8") as f:
        f.write(f"[{waktu}]\nUSER : {user_input}\nAGENT: {agent_output}\n{'-'*30}\n")

# --- 3. FUNGSI PLAN (Updated with Multi-step) ---
def plan(user_input: str):
    teks = user_input.lower().strip()
    langkah = []

    # A. Multi-step: Buat Quiz
    if "buat quiz dari file" in teks:
        path = teks.replace("buat quiz dari file", "").strip()
        langkah = [("baca_file", path), ("buat_soal", None)]
    
    # B. Multi-step: Konversi Suhu Massal
    elif "konversi suhu dari file" in teks:
        path = teks.replace("konversi suhu dari file", "").strip()
        langkah = [("baca_file", path), ("konversi_suhu_massal", None)]
    
    # C. Multi-step: Cari Kata & Tampilkan Ringkas
    elif "cari kata" in teks and " di file " in teks:
        match = re.search(r"cari kata (.+) di file (.+)", teks)
        if match:
            kata, path = match.groups()
            langkah = [("baca_file", path.strip()), ("hitung_kata_ringkas", kata.strip())]

    # D. Bonus: Task List Perintah
    elif teks.startswith("tambah task"):
        judul = teks.replace("tambah task", "").strip()
        langkah = [("add_task", judul)]
    elif teks == "lihat task":
        langkah = [("show_tasks", None)]

    # E. Perintah Tunggal (Existing)
    elif teks == "hapus memori": langkah = [("clear_memory", None)]
    elif teks == "ringkas chat": langkah = [("memory_summary", None)]
    elif "ringkas file" in teks:
        path = teks.replace("ringkas file", "").strip()
        langkah = [("baca_file", path), ("ringkas_teks", None)]
    elif "analisis nilai file" in teks:
        path = teks.replace("analisis nilai file", "").strip()
        langkah = [("baca_file", path), ("hitung_rata2", None)]
    else:
        langkah = [("panggil_tool", teks)]
    
    return langkah

# --- 4. FUNGSI ACT (Updated with New Tools) ---
def act(step, context):
    nama_tool, arg = step

    if nama_tool == "baca_file": return baca_file(arg)
    
    # --- New Multi-step Tools ---
    if nama_tool == "buat_soal":
        teks = context.get("last_output", "")
        if "tidak ditemukan" in teks: return teks
        # Ambil 3 kalimat pertama sebagai basis soal
        poin = [p.strip() for p in teks.split('.') if len(p.strip()) > 5][:3]
        quiz = "--- QUIZ DARI FILE ---\n"
        for i, p in enumerate(poin):
            quiz += f"Soal {i+1}: Jelaskan maksud dari kalimat '{p[:40]}...'?\n"
        return quiz

    if nama_tool == "konversi_suhu_massal":
        teks = context.get("last_output", "")
        angka_list = re.findall(r"[-+]?\d*\.\d+|\d+", teks)
        if not angka_list: return "Tidak ada angka suhu ditemukan."
        hasil = "Konversi Suhu Massal (C ke F):\n"
        for a in angka_list:
            f = (float(a) * 9/5) + 32
            hasil += f"- {a}°C = {f:.2f}°F\n"
        return hasil

    if nama_tool == "hitung_kata_ringkas":
        teks = context.get("last_output", "")
        count = teks.lower().count(arg.lower())
        kalimat = [s.strip() for s in teks.split('.') if s.strip()]
        ringkas = ". ".join(kalimat[:1]) + "."
        return f"Kata '{arg}' muncul {count} kali.\nRingkasan: {ringkas}"

    # --- Bonus: Task List Logic ---
    if nama_tool == "add_task":
        tasks = []
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f: tasks = json.load(f)
        tasks.append({"judul": arg, "waktu": datetime.now().strftime("%H:%M")})
        with open("tasks.json", "w") as f: json.dump(tasks, f, indent=2)
        return f"Task '{arg}' ditambahkan!"

    if nama_tool == "show_tasks":
        if not os.path.exists("tasks.json"): return "Task list kosong."
        with open("tasks.json", "r") as f: 
            data = json.load(f)
            return "Daftar Tugas:\n" + "\n".join([f"- {t['judul']} ({t['waktu']})" for t in data])

    # --- Existing Tools ---
    if nama_tool == "clear_memory":
        global memory_chat
        memory_chat = []
        save_memory()
        return "Memori dibersihkan!"
    
    if nama_tool == "memory_summary":
        chats = memory_chat[-5:]
        if not chats: return "Belum ada riwayat."
        return "\n".join([f"{'Anda' if c['role']=='user' else 'Agent'}: {c['content']}" for c in chats])

    if nama_tool == "ringkas_teks":
        teks = context.get("last_output", "")
        kalimat = [s.strip() for s in teks.split('.') if s.strip()]
        return ". ".join(kalimat[:2]) + "." if kalimat else "File kosong."

    if nama_tool == "hitung_rata2":
        teks = context.get("last_output", "")
        angka = [float(s) for s in re.findall(r"[-+]?\d*\.\d+|\d+", teks)]
        return f"Rata-rata: {sum(angka)/len(angka):.2f}" if angka else "Tidak ada angka."

    if nama_tool == "panggil_tool":
        teks = arg
        if any(c.isdigit() for c in teks) and any(op in teks for op in "+-*/"):
            return f"Hasil: {kalkulator(teks)}"
        if "bmi" in teks:
            num = re.findall(r"\d+", teks)
            return hitung_bmi(float(num[0]), float(num[1])) if len(num) >= 2 else "Input BMI salah."
        if "suhu" in teks:
            match = re.search(r"(\d+).+ke\s+([cf])", teks)
            return konversi_suhu(float(match.group(1)), match.group(2)) if match else "Input suhu salah."
        if "arti" in teks:
            return kamus_lookup(teks.replace("arti", "").strip())
        return "Gunakan kata kunci: hitung, bmi, suhu, arti, ringkas file, quiz, konversi suhu dari file, atau task."

# --- 5. RUN AGENT (With Trace Summary) ---
def run_agent(user_input):
    langkah_kerja = plan(user_input)
    context = {"last_output": None}
    trace = []

    print(f"[*] Thinking... Plan: {langkah_kerja}")

    for step in langkah_kerja:
        trace.append(step[0])
        result = act(step, context)
        context["last_output"] = result
        if isinstance(result, str) and ("Error" in result or "tidak ditemukan" in result):
            return f"Gagal pada {step[0]}: {result}"

    final_output = context.get("last_output", "")
    trace_summary = f"\n[Trace: {' -> '.join(trace)}]"
    return str(final_output) + trace_summary

# --- 6. MAIN LOOP ---
if __name__ == "__main__":
    load_memory()
    print("=== Agent ReAct Multi-Step System Ready ===")
    while True:
        try:
            q = input("\nKamu: ")
            if not q.strip(): continue
            if q.lower() in ["exit", "quit"]: break
            
            hasil = run_agent(q)
            print("Agent:", hasil)
            log_interaksi(q, hasil)
            
            if q.lower() not in ["ringkas chat", "hapus memori", "lihat task"]:
                simpan_chat("user", q)
                simpan_chat("agent", hasil)
        except KeyboardInterrupt:
            break