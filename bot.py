import math
import random
import re
import sqlite3
import unittest
import logging
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog, messagebox
import json
import os
import datetime
import urllib.request
import sys
import subprocess
import pygame

# Global variable to track currently playing music file
current_music_file = [None]

logging.basicConfig(
    filename="fika_error.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

PENGETAHUAN_URL = "https://raw.githubusercontent.com/username/repo/main/pengetahuan.json"  # Ganti dengan URL JSON online

DEVELOPER_MODE = "--dev" in sys.argv

if DEVELOPER_MODE:
    logging.getLogger().setLevel(logging.DEBUG)
    print("Developer mode aktif. Log akan tampil di console.")

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("riwayat_fika.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS riwayat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pertanyaan TEXT,
            jawaban TEXT,
            waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS pengetahuan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pertanyaan TEXT,
            jawaban TEXT
        )
    """)
    conn.commit()
    conn.close()

def simpan_riwayat(pertanyaan, jawaban):
    try:
        conn = sqlite3.connect("riwayat_fika.db")
        c = conn.cursor()
        c.execute("INSERT INTO riwayat (pertanyaan, jawaban) VALUES (?, ?)", (pertanyaan, jawaban))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Gagal menyimpan riwayat:", e)

def simpan_pengetahuan(pertanyaan, jawaban):
    try:
        conn = sqlite3.connect("riwayat_fika.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS pengetahuan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pertanyaan TEXT,
                jawaban TEXT
            )
        """)
        c.execute("INSERT INTO pengetahuan (pertanyaan, jawaban) VALUES (?, ?)", (pertanyaan.lower(), jawaban))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Gagal menyimpan pengetahuan:", e)

def tampilkan_riwayat(limit=10):
    try:
        conn = sqlite3.connect("riwayat_fika.db")
        c = conn.cursor()
        c.execute("SELECT waktu, pertanyaan, jawaban FROM riwayat ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        if not rows:
            print("Belum ada riwayat.")
            return
        print("\n--- Riwayat Tanya Jawab Terakhir ---")
        for waktu, tanya, jawab in rows[::-1]:
            print(f"[{waktu}]")
            print(f"Tanya: {tanya}")
            print(f"Jawab: {jawab}\n")
    except Exception as e:
        print("Gagal menampilkan riwayat:", e)

def cari_pengetahuan(pertanyaan):
    try:
        conn = sqlite3.connect("riwayat_fika.db")
        c = conn.cursor()
        c.execute("""
            SELECT jawaban FROM pengetahuan WHERE pertanyaan=?
        """, (pertanyaan.lower(),))
        row = c.fetchone()
        conn.close()
        if row:
            return row[0]
    except Exception:
        pass
    return None

# --- Utility & Fitur Lain ---
def input_angka(prompt, allow_negative=False):
    while True:
        try:
            val = float(input(prompt))
            if not allow_negative and val < 0:
                print("Angka tidak boleh negatif.")
                continue
            return val
        except ValueError:
            print("Input tidak valid, coba lagi.")

def tampilkan_cuaca():
    kondisi = ["cerah", "berawan", "hujan ringan", "hujan deras", "berkabut"]
    suhu = random.randint(25, 35)
    return f"Hari ini cuacanya {random.choice(kondisi)} dengan suhu sekitar {suhu}°C."

def tampilkan_fakta():
    fakta = [
        "SoC Dimensity 9300 punya performa lebih tinggi dari Snapdragon 8 Gen 2.",
        "GPU Adreno dibuat oleh Qualcomm dan digunakan di banyak HP Android.",
        "CPU modern punya beberapa core untuk multitasking.",
        "Smartphone flagship biasanya punya refresh rate 120Hz untuk layar lebih halus.",
        "Baterai lithium-ion lebih awet jika tidak diisi penuh 100% terus-menerus."
    ]
    return "Fakta teknologi hari ini:\n" + random.choice(fakta)

def cek_faktorial(tanya):
    match = re.search(r'(-?\d+)\s*!', tanya)
    if match:
        angka = int(match.group(1))
        if angka < 0:
            return "Faktorial hanya untuk bilangan bulat non-negatif ya."
        try:
            hasil = math.factorial(angka)
            return f"{angka}! = {hasil}"
        except Exception:
            return "Maaf, terjadi kesalahan saat menghitung faktorial."
    return None

def cek_hitung(tanya):
    allowed = "0123456789+-*/(). "
    ekspresi = "".join(c for c in tanya if c in allowed)
    if ekspresi.strip() == "":
        return None
    try:
        hasil = eval(ekspresi)
        return f"Hasil perhitungannya adalah {hasil}"
    except Exception:
        return None

def load_pengetahuan_file():
    path = os.path.join(os.path.dirname(__file__), "pengetahuan.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def cek_keyword(tanya):
    tanya = tanya.lower()
    pengetahuan = load_pengetahuan_file()
    for kunci, jawaban in pengetahuan.items():
        if kunci.lower() in tanya:
            return jawaban
    return None

def simpan_pengetahuan_file(pertanyaan, jawaban):
    path = os.path.join(os.path.dirname(__file__), "pengetahuan.json")
    data = load_pengetahuan_file()
    data[pertanyaan.lower()] = jawaban
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def tampilkan_fakta_menarik():
    path = os.path.join(os.path.dirname(__file__), "fakta_menarik.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            fakta_list = json.load(f)
        if not fakta_list:
            return "Belum ada fakta menarik."
        return "Fakta menarik hari ini:\n" + random.choice(fakta_list)
    except Exception:
        return "Gagal membaca fakta menarik."

def pastikan_file_json():
    for fname, default in [
        ("pengetahuan.json", {}),
        ("fakta_menarik.json", [])
    ]:
        path = os.path.join(os.path.dirname(__file__), fname)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default, f, ensure_ascii=False, indent=2)

def update_pengetahuan_online():
    try:
        response = urllib.request.urlopen(PENGETAHUAN_URL, timeout=5)
        data = response.read().decode("utf-8")
        pengetahuan = json.loads(data)
        path = os.path.join(os.path.dirname(__file__), "pengetahuan.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pengetahuan, f, ensure_ascii=False, indent=2)
        print("Pengetahuan berhasil diperbarui dari internet.")
        return True
    except Exception as e:
        print("Gagal update pengetahuan online:", e)
        return False

def tanya_fika():
    print("\n=== Tanya Fika ===")
    print("Ketik 'esc' untuk kembali ke menu utama.")
    while True:
        tanya = input("Kamu (Akiro): ").lower()

        if "esc" in tanya:
            print("Fika: Oke, kita kembali ke menu utama ya.")
            break

        for cek_func in (cek_faktorial, cek_hitung, cek_keyword):
            jawaban = cek_func(tanya)
            if jawaban:
                print("Fika:", jawaban)
                simpan_riwayat(tanya, jawaban)
                break
        else:
            print("Fika: Maaf, aku belum mengerti pertanyaanmu.")
            saran = [
                "Coba tanya tentang faktorial misal '5!'",
                "hitung matematika seperti '2+3*4', atau fakta teknologi.",
                "teknologi seputar smartphone, atau soal geometri.",
                "atau tanya tentang apa yang Fika bisa lakukan.",
                "atau tanya tentang 'Fika bisa apa'.",
                "atau tanya tentang 'spek vivo v21 5g'.",       
                "atau tanya tentang presiden Indonesia, ibukota Indonesia, atau gravitasi.",
                "atau tanya tentang fotosintesis, komputer, atau halo.",
                "atau tanya tentang spesifikasi smartphone seperti 'spek vivo v21 5g'.",
                "atau jika ingin kembali ketik 'esc' ya"
            ]
            print(f" {random.choice(saran)} ")

def kalkulator():
    operasi = {
        "1": ("Penjumlahan", lambda a, b: a + b),
        "2": ("Pengurangan", lambda a, b: a - b),
        "3": ("Perkalian", lambda a, b: a * b),
        "4": ("Pembagian", lambda a, b: a / b if b != 0 else "Pembagian dengan nol tidak diperbolehkan."),
        "6": ("Pangkat", lambda a, b: a ** b)
    }
    while True:
        print("\n=== Kalkulator ===")
        print("1. Penjumlahan (+)")
        print("2. Pengurangan (-)")
        print("3. Perkalian (*)")
        print("4. Pembagian (/)")
        print("5. Akar Kuadrat")
        print("6. Pangkat")
        print("7. Kembali ke menu utama")

        pilih = input("Pilih operasi (1-7): ")

        if pilih == "7":
            break

        if pilih in operasi:
            a = input_angka("Masukkan angka pertama: ")
            b = input_angka("Masukkan angka kedua: ")
            hasil = operasi[pilih][1](a, b)
            print(f"Hasil: {hasil}")
        elif pilih == "5":
            a = input_angka("Masukkan angka: ")
            if a < 0:
                print("Tidak bisa menghitung akar kuadrat dari angka negatif.")
            else:
                print(f"Hasil akar kuadrat dari {a} adalah {math.sqrt(a)}")
        else:
            print("Pilihan tidak valid.")

def keliling_persegi():
    sisi = input_angka("Masukkan sisi: ")
    print(f"Keliling Persegi = {4 * sisi}")

def keliling_persegi_panjang():
    p = input_angka("Panjang: ")
    l = input_angka("Lebar: ")
    print(f"Keliling Persegi Panjang = {2 * (p + l)}")

def keliling_lingkaran():
    r = input_angka("Jari-jari: ")
    print(f"Keliling Lingkaran = {2 * math.pi * r:.2f}")

def keliling_segitiga():
    a = input_angka("Sisi a: ")
    b = input_angka("Sisi b: ")
    c = input_angka("Sisi c: ")
    print(f"Keliling Segitiga = {a + b + c}")

def luas_persegi():
    sisi = input_angka("Masukkan sisi: ")
    print(f"Luas Persegi = {sisi * sisi}")

def luas_persegi_panjang():
    p = input_angka("Panjang: ")
    l = input_angka("Lebar: ")
    print(f"Luas Persegi Panjang = {p * l}")

def luas_lingkaran():
    r = input_angka("Jari-jari: ")
    print(f"Luas Lingkaran = {math.pi * r * r:.2f}")

def luas_segitiga():
    a = input_angka("Alas: ")
    t = input_angka("Tinggi: ")
    print(f"Luas Segitiga = {0.5 * a * t}")

def volume_kubus():
    sisi = input_angka("Masukkan sisi: ")
    print(f"Volume Kubus = {sisi ** 3}")

def volume_balok():
    p = input_angka("Panjang: ")
    l = input_angka("Lebar: ")
    t = input_angka("Tinggi: ")
    print(f"Volume Balok = {p * l * t}")

def volume_tabung():
    r = input_angka("Jari-jari: ")
    t = input_angka("Tinggi: ")
    print(f"Volume Tabung = {math.pi * r**2 * t:.2f}")

def volume_kerucut():
    r = input_angka("Jari-jari: ")
    t = input_angka("Tinggi: ")
    print(f"Volume Kerucut = {(1/3) * math.pi * r**2 * t:.2f}")

keliling_map = {
    "a": keliling_persegi,
    "b": keliling_persegi_panjang,
    "c": keliling_lingkaran,
    "d": keliling_segitiga
}
luas_map = {
    "a": luas_persegi,
    "b": luas_persegi_panjang,
    "c": luas_lingkaran,
    "d": luas_segitiga
}
volume_map = {
    "a": volume_kubus,
    "b": volume_balok,
    "c": volume_tabung,
    "d": volume_kerucut
}

def geometri():
    while True:
        print("\n=== Geometri ===")
        print("1. Keliling Bangun Datar")
        print("2. Luas Bangun Datar")
        print("3. Volume Bangun Ruang")
        print("4. Kembali ke menu utama")

        pilih = input("Pilih menu (1-4): ")

        if pilih == "4":
            break

        if pilih in ["1", "2", "3"]:
            if pilih == "1":
                print("\nPilih bangun datar:")
                print("a. Persegi")
                print("b. Persegi Panjang")
                print("c. Lingkaran")
                print("d. Segitiga")
                bangun = input("Pilih (a-d): ").lower()
                func = keliling_map.get(bangun)
            elif pilih == "2":
                print("\nPilih bangun datar:")
                print("a. Persegi")
                print("b. Persegi Panjang")
                print("c. Lingkaran")
                print("d. Segitiga")
                bangun = input("Pilih (a-d): ").lower()
                func = luas_map.get(bangun)
            elif pilih == "3":
                print("\nPilih bangun ruang:")
                print("a. Kubus")
                print("b. Balok")
                print("c. Tabung")
                print("d. Kerucut")
                bangun = input("Pilih (a-d): ").lower()
                func = volume_map.get(bangun)
            if func:
                func()
            else:
                print("Pilihan tidak valid.")
        else:
            print("Pilihan tidak valid.")

def menu_utama():
    while True:
        print("\n=== Menu Utama ===")
        print("1. Tanya Fika")
        print("2. Kalkulator")
        print("3. Geometri")
        print("4. Cuaca Hari Ini")
        print("5. Fakta Teknologi")
        print("6. Fakta Menarik")
        print("7. Lihat Riwayat Tanya Jawab")
        print("8. Pemutar Musik")
        print("9. Keluar")

        pilih = input("Pilih menu (1-9): ").strip()

        if pilih == "1":
            tanya_fika()
        elif pilih == "2":
            kalkulator()
        elif pilih == "3":
            geometri()
        elif pilih == "4":
            print(tampilkan_cuaca())
        elif pilih == "5":
            print(tampilkan_fakta())
        elif pilih == "6":
            print(tampilkan_fakta_menarik())
        elif pilih == "7":
            tampilkan_riwayat()
        elif pilih == "8":
            play_music_file()
        elif pilih == "9":
            print("Sampai jumpa, Akiro!")
            break
        else:
            print("Pilihan tidak valid.")

def play_music_file():
    print("\n=== Pemutar Musik Sederhana ===")
    print("Masukkan path file musik (mp3/wav) atau ketik 'kembali' untuk kembali ke menu.")
    while True:
        file_path = input("Path file musik: ").strip()
        if file_path.lower() == "kembali":
            break
        if not os.path.isfile(file_path):
            print("File tidak ditemukan. Coba lagi.")
            continue
        try:
            # Windows: gunakan start, Linux/Mac: gunakan xdg-open/open
            if sys.platform.startswith("win"):
                os.startfile(file_path)
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])
            current_music_file[0] = file_path
            print(f"Memutar musik: {os.path.basename(file_path)}. Tutup aplikasi pemutar untuk memilih lagu lain.")
            break
        except Exception as e:
            print(f"Gagal memutar musik: {e}")

# Inisialisasi pygame mixer sekali saja
pygame.mixer.init()

# Tambahkan di atas fungsi mulai_gui
playlist = []
playlist_index = [0]

def tambah_ke_playlist(file_paths):
    for path in file_paths:
        if path and os.path.isfile(path):
            playlist.append(path)

def putar_lagu_playlist(index):
    if 0 <= index < len(playlist):
        try:
            pygame.mixer.music.load(playlist[index])
            pygame.mixer.music.play()
            current_music_file[0] = playlist[index]
            return True
        except Exception:
            return False
    return False

def lagu_selanjutnya():
    if playlist:
        playlist_index[0] = (playlist_index[0] + 1) % len(playlist)
        putar_lagu_playlist(playlist_index[0])

def lagu_sebelumnya():
    if playlist:
        playlist_index[0] = (playlist_index[0] - 1) % len(playlist)
        putar_lagu_playlist(playlist_index[0])

def mulai_gui():
    global root, chat_area, entry
    root = tk.Tk()
    root.title("Fika Chatbot")
    root.configure(bg="#e3f2fd")

    def tanya_fika_logic(tanya):
        tanya = tanya.lower()
        # Deteksi pertanyaan tentang lagu/musik yang sedang diputar
        if any(k in tanya for k in [
            "lagu apa yang sedang diputar",
            "musik apa yang sedang diputar",
            "apa yang sedang diputar",
            "judul lagu yang diputar",
            "lagu sekarang",
            "lagu apa ini"
        ]):
            if current_music_file[0]:
                return f"Saat ini sedang memutar: {os.path.basename(current_music_file[0])}"
            else:
                return "Tidak ada musik yang sedang diputar."
        for cek_func in (cek_faktorial, cek_hitung, cek_keyword):
            jawaban = cek_func(tanya)
            if jawaban:
                simpan_riwayat(tanya, jawaban)
                return jawaban
        return "Maaf, aku belum mengerti pertanyaanmu."

    def kirim():
        user_msg = entry.get().strip()
        if not user_msg:
            return
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"Kamu: {user_msg}\n")
        chat_area.config(state='disabled')
        chat_area.see(tk.END)
        bot_reply = tanya_fika_logic(user_msg)
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"Fika: {bot_reply}\n")
        chat_area.config(state='disabled')
        chat_area.see(tk.END)
        entry.delete(0, tk.END)

    # Judul
    title = tk.Label(root, text="Fika Chatbot", font=("Segoe UI", 18, "bold"), bg="#e3f2fd", fg="#1565c0")
    title.pack(pady=(10,0))

    chat_area = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled', wrap=tk.WORD, font=("Consolas", 11), bg="#f5f5f5")
    chat_area.pack(padx=10, pady=10)

    frame = tk.Frame(root, bg="#e3f2fd")
    frame.pack(padx=10, pady=(0,10), fill='x')

    entry = tk.Entry(frame, width=45, font=("Segoe UI", 11))
    entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0,5))
    entry.focus()

    send_btn = tk.Button(frame, text="Kirim", command=kirim, bg="#1976d2", fg="white", font=("Segoe UI", 10, "bold"))
    send_btn.pack(side=tk.LEFT)

    # Tombol Fakta Menarik
    def tampilkan_fakta_gui():
        fakta = tampilkan_fakta_menarik()
        chat_area.config(state='normal')
        chat_area.insert(tk.END, f"Fika (Fakta Menarik): {fakta}\n")
        chat_area.config(state='disabled')
        chat_area.see(tk.END)

    fakta_btn = tk.Button(root, text="Fakta Menarik", command=tampilkan_fakta_gui, bg="#8e24aa", fg="white", font=("Segoe UI", 10, "bold"))
    fakta_btn.pack(pady=(0,10))

    # --- Pemutar Musik Native ---
    music_status = tk.StringVar(value="Tidak ada musik yang diputar.")

    def pilih_dan_tambah_playlist():
        file_paths = filedialog.askopenfilenames(
            title="Pilih file musik (bisa lebih dari satu)",
            filetypes=[("Audio", "*.mp3 *.wav *.ogg *.flac"), ("Semua File", "*.*")]
        )
        tambah_ke_playlist(file_paths)
        if playlist:
            music_status.set(f"Playlist: {len(playlist)} lagu. Klik ▶️ untuk mulai.")
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"Fika: {len(file_paths)} lagu ditambahkan ke playlist.\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)

    def putar_playlist():
        if not playlist:
            music_status.set("Playlist kosong.")
            return
        if putar_lagu_playlist(playlist_index[0]):
            music_status.set(f"Memutar: {os.path.basename(playlist[playlist_index[0]])} ({playlist_index[0]+1}/{len(playlist)})")
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"Fika: Memutar musik: {os.path.basename(playlist[playlist_index[0]])}\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)
        else:
            music_status.set("Gagal memutar lagu.")

    def pause_musik():
        pygame.mixer.music.pause()
        music_status.set("Musik dijeda.")

    def lanjut_musik():
        pygame.mixer.music.unpause()
        if playlist:
            music_status.set(f"Memutar: {os.path.basename(playlist[playlist_index[0]])} ({playlist_index[0]+1}/{len(playlist)})")

    def stop_musik():
        pygame.mixer.music.stop()
        music_status.set("Tidak ada musik yang diputar.")
        current_music_file[0] = None

    def next_musik():
        if playlist:
            lagu_selanjutnya()
            putar_playlist()

    def prev_musik():
        if playlist:
            lagu_sebelumnya()
            putar_playlist()

    music_frame = tk.Frame(root, bg="#e3f2fd")
    music_frame.pack(pady=(0,10))

    add_btn = tk.Button(music_frame, text="➕ Tambah Lagu", command=pilih_dan_tambah_playlist, bg="#009688", fg="white", font=("Segoe UI", 10, "bold"))
    add_btn.pack(side=tk.LEFT, padx=2)
    play_btn = tk.Button(music_frame, text="▶️ Mainkan", command=putar_playlist, bg="#43a047", fg="white", font=("Segoe UI", 10, "bold"))
    play_btn.pack(side=tk.LEFT, padx=2)
    pause_btn = tk.Button(music_frame, text="⏸️ Pause", command=pause_musik, bg="#fbc02d", fg="black", font=("Segoe UI", 10, "bold"))
    pause_btn.pack(side=tk.LEFT, padx=2)
    lanjut_btn = tk.Button(music_frame, text="▶️ Lanjut", command=lanjut_musik, bg="#0288d1", fg="white", font=("Segoe UI", 10, "bold"))
    lanjut_btn.pack(side=tk.LEFT, padx=2)
    prev_btn = tk.Button(music_frame, text="⏮️ Prev", command=prev_musik, bg="#607d8b", fg="white", font=("Segoe UI", 10, "bold"))
    prev_btn.pack(side=tk.LEFT, padx=2)
    next_btn = tk.Button(music_frame, text="⏭️ Next", command=next_musik, bg="#607d8b", fg="white", font=("Segoe UI", 10, "bold"))
    next_btn.pack(side=tk.LEFT, padx=2)
    stop_btn = tk.Button(music_frame, text="⏹️ Stop", command=stop_musik, bg="#d32f2f", fg="white", font=("Segoe UI", 10, "bold"))
    stop_btn.pack(side=tk.LEFT, padx=2)
    status_lbl = tk.Label(music_frame, textvariable=music_status, bg="#e3f2fd", fg="#333", font=("Segoe UI", 10, "italic"))
    status_lbl.pack(side=tk.LEFT, padx=10)

    # --- Tema ---
    def set_theme(mode="light"):
        if mode == "dark":
            root.configure(bg="#222")
            chat_area.configure(bg="#333", fg="#eee", insertbackground="#eee")
            entry.configure(bg="#222", fg="#eee", insertbackground="#eee")
            title.configure(bg="#222", fg="#ffb300")
            frame.configure(bg="#222")
        else:
            root.configure(bg="#e3f2fd")
            chat_area.configure(bg="#f5f5f5", fg="#222", insertbackground="#222")
            entry.configure(bg="white", fg="#222", insertbackground="#222")
            title.configure(bg="#e3f2fd", fg="#1565c0")
            frame.configure(bg="#e3f2fd")

    theme_mode = ["light"]
    def toggle_theme():
        theme_mode[0] = "dark" if theme_mode[0] == "light" else "light"
        set_theme(theme_mode[0])

    theme_btn = tk.Button(root, text="🌙/☀️", command=toggle_theme, bg="#607d8b", fg="white")
    theme_btn.pack(pady=(0,5))

    root.bind('<Return>', lambda event: kirim())

    root.mainloop()

# --- Unit Test ---
class TestBot(unittest.TestCase):
    def test_cek_faktorial(self):
        self.assertEqual(cek_faktorial("5!"), "5! = 120")
        self.assertIn("Faktorial hanya untuk bilangan bulat non-negatif", cek_faktorial("-3!"))

    def test_cek_hitung(self):
        self.assertEqual(cek_hitung("2+3*4"), "Hasil perhitungannya adalah 14")
        self.assertIsNone(cek_hitung("abc"))

    def test_cek_keyword(self):
        self.assertIn("Presiden Indonesia", cek_keyword("siapa presiden indonesia?"))
        self.assertIsNone(cek_keyword("pertanyaan tidak dikenal"))

# --- Main ---
if __name__ == "__main__":
    init_db()
    pastikan_file_json()
    mode = input("Ketik 'gui' untuk mode GUI, atau tekan Enter untuk mode terminal: ").strip().lower()
    if mode == "gui":
        mulai_gui()
    else:
        menu_utama()
