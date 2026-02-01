import ast
import operator

def kalkulator(expr: str):
    """Mengevaluasi ekspresi matematika dengan aman."""
    if not expr.strip(): return "Ekspresi kosong."
    operators = {
        ast.Add: operator.add, ast.Sub: operator.sub, 
        ast.Mult: operator.mul, ast.Div: operator.truediv, 
        ast.Pow: operator.pow, ast.USub: operator.neg
    }
    def eval_expr(node):
        if isinstance(node, ast.Constant): return node.value
        elif hasattr(ast, 'Num') and isinstance(node, ast.Num): return node.n
        elif isinstance(node, ast.BinOp): 
            return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp): 
            return operators[type(node.op)](eval_expr(node.operand))
        else: raise TypeError(f"Tipe {type(node).__name__} tidak didukung")
    try:
        tree = ast.parse(expr, mode='eval')
        return eval_expr(tree.body)
    except Exception as e:
        return f"Error: {e}"

KAMUS = {
    "python": "Bahasa pemrograman populer untuk otomasi, data, dan AI.",
    "agent": "Program yang bisa merencanakan dan memakai tool untuk menyelesaikan tujuan.",
    "llm": "Model bahasa besar yang menghasilkan teks berdasarkan konteks."
}

def kamus_lookup(kata: str) -> str:
    return KAMUS.get(kata.lower().strip(), "Kata tidak ditemukan di kamus.")

def baca_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError: return "File tidak ditemukan."
    except Exception as e: return f"Error: {e}"

# --- MINI EXERCISE: TOOL BARU ---

def konversi_suhu(nilai: float, ke: str) -> str:
    """Konversi C ke F atau sebaliknya."""
    if ke.lower() == "f":
        return f"{nilai}°C = {(nilai * 9/5) + 32:.2f}°F"
    return f"{nilai}°F = {(nilai - 32) * 5/9:.2f}°C"

def hitung_bmi(berat: float, tinggi_cm: float) -> str:
    """Hitung BMI berdasarkan berat(kg) dan tinggi(cm)."""
    bmi = berat / ((tinggi_cm / 100) ** 2)
    status = "Ideal" if 18.5 <= bmi < 25 else "Luar Ideal"
    return f"BMI: {bmi:.2f} ({status})"

def hitung_kata_file(path: str, kata: str) -> str:
    """Menghitung kemunculan kata dalam file."""
    konten = baca_file(path)
    if "Error" in konten or "tidak ditemukan" in konten: return konten
    count = konten.lower().count(kata.lower())
    return f"Kata '{kata}' ditemukan {count} kali di {path}."