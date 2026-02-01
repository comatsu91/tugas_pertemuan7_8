import json
import os

MEMORY_FILE = "memory_chat.json"

def load_tasks():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(MEMORY_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def tambah_task(judul):
    tasks = load_tasks()
    tasks.append({"judul": judul})
    save_tasks(tasks)
    return "Task berhasil ditambahkan."

def lihat_task():
    tasks = load_tasks()
    if not tasks:
        return "Belum ada task."
    return "\n".join(f"- {t['judul']}" for t in tasks)

if __name__ == "__main__":
    command = input("Masukkan perintah: ")

    if command.startswith("tambah task"):
        judul = command.replace("tambah task", "").strip()
        print(tambah_task(judul))

    elif command == "lihat task":
        print(lihat_task())
