from tools import kalkulator, kamus_lookup, baca_file

def plan(user_input: str):
    teks = user_input.lower().strip()
    langkah = []

    # rencana sederhana berbasis kata kunci
    if teks.startswith("buat ringkasan file "):
        path = teks.replace("buat ringkasan file", "").strip()
        langkah.append(("baca_file", path))
        langkah.append(("ringkas_teks", None))
        return langkah

    if teks.startswith("analisis nilai file "):
        path = teks.replace("analisis nilai file", "").strip()
        langkah.append(("baca_file", path))
        langkah.append(("hitung_rata2", None))
        return langkah

    # fallback: satu langkah
    langkah.append(("jawab_langsung", teks))
    return langkah

def act(step, context):
    nama_tool, arg = step

    if nama_tool == "baca_file":
        return baca_file(arg)

    if nama_tool == "ringkas_teks":
        teks = context.get("last_output", "")
        # ringkas rule-based: ambil 2 kalimat pertama
        kalimat = teks.split(".")
        ringkas = ".".join(kalimat[:2]).strip()
        return ringkas + "."

    if nama_tool == "hitung_rata2":
        teks = context.get("last_output", "")
        # ambil angka dari teks (asumsi satu angka per baris)
        angka = []
        for line in teks.splitlines():
            try:
                angka.append(float(line.strip()))
            except:
                pass
        if len(angka) == 0:
            return "Tidak ada angka yang bisa dihitung."
        return sum(angka) / len(angka)

    if nama_tool == "jawab_langsung":
        return "Saya belum paham tugas itu. Coba perintah yang jelas."

def observe(result, context):
    context["last_output"] = result

def reflect(context):
    # refleksi sederhana: cek error umum
    out = context.get("last_output", "")
    if isinstance(out, str) and "Error" in out:
        context["need_retry"] = True
    else:
        context["need_retry"] = False

def run_agent(user_input):
    langkah = plan(user_input)
    context = {}

    for step in langkah:
        result = act(step, context)
        observe(result, context)
        reflect(context)

        if context.get("need_retry"):
            return "Langkah gagal, silakan cek input atau file."

    return context.get("last_output", "")

while True:
    q = input("\nKamu: ")
    if q.lower() in ["exit", "quit"]:
        print("Agent berhenti.")
        break
    print("Agent:", run_agent(q))